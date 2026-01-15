import bpy
import subprocess
import requests
import sys
import threading
import time
from .logger import logger

# Replace this with your actual Vercel URL
API_URL = "https://sklum-license-backend.vercel.app/api/index"

# Global cache for HWID to prevent multiple slow subprocess calls
_cached_hwid = None

# Background validation results
_validation_thread = None
_validation_result = None  # (is_valid, message, timestamp)

def get_machine_id():
    """Gets a unique ID for the machine (Windows UUID)."""
    global _cached_hwid
    if _cached_hwid:
        return _cached_hwid

    # Method 1: WMIC (Standard)
    try:
        cmd = "wmic csproduct get uuid"
        output = subprocess.check_output(cmd, shell=True, timeout=5).decode()
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1:
            _cached_hwid = lines[1]
            return _cached_hwid
    except:
        pass

    # Method 2: PowerShell (Modern Windows)
    try:
        cmd = 'powershell "Get-CimInstance -Class Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"'
        uuid_str = subprocess.check_output(cmd, shell=True, timeout=5).decode().strip()
        if uuid_str:
            _cached_hwid = uuid_str
            return _cached_hwid
    except:
        pass
        
    # Method 3: MAC Address (Fallback)
    try:
        import uuid
        _cached_hwid = str(uuid.getnode())
        return _cached_hwid
    except:
        pass

    return "UNKNOWN_HWID_ERROR"

def validate_license(key):
    """
    Validates the license key against the server. (Synchronous/Blocking)
    """
    if not key:
        return False, "Vui lòng nhập License Key."
    
    hwid = get_machine_id()
    payload = {
        'key': key.strip(),
        'hwid': hwid
    }
    
    try:
        logger.info(f"Validating license key: {key[:4]}... with HWID: {hwid}")
        response = requests.post(API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return True, data.get('message', "License Valid")
        else:
            try:
                data = response.json()
                msg = data.get('message', f"Error {response.status_code}")
                return False, msg
            except:
                return False, f"Server Error {response.status_code}"
                
    except requests.exceptions.Timeout:
        return False, "Hết thời gian kết nối (Timeout)."
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối đến Server."
    except Exception as e:
        return False, f"Lỗi không xác định: {str(e)}"

def _validation_worker(key):
    global _validation_result
    is_valid, message = validate_license(key)
    _validation_result = (is_valid, message, time.time())

def validate_license_async(key):
    """Starts a background thread for license validation."""
    global _validation_thread, _validation_result
    
    if _validation_thread and _validation_thread.is_alive():
        return False # Already running
    
    _validation_result = None
    _validation_thread = threading.Thread(target=_validation_worker, args=(key,), daemon=True)
    _validation_thread.start()
    return True

def get_async_result():
    """Returns the result if the thread has finished, otherwise None."""
    global _validation_result
    return _validation_result

def _poll_activation_result():
    """Timer callback to check for async validation results."""
    res = get_async_result()
    if res is None:
        # Still running, check again in 0.5s
        return 0.5
    
    # Validation finished
    is_valid, msg, timestamp = res
    if is_valid:
        try:
            # Sync to Scene state
            scene = bpy.context.scene
            if hasattr(scene, "sklum"):
                scene.sklum.license_active = True
                scene.sklum.license_message = msg
                
                # Also populate the scene property key from prefs for UI consistency
                addon_name = __package__.split('.core')[0]
                prefs = bpy.context.preferences.addons.get(addon_name)
                if prefs:
                    scene.sklum.license_key = prefs.preferences.license_key

            logger.info(f"Auto-activation successful: {msg}")
        except Exception as e:
            logger.error(f"Failed to apply license state: {e}")
    else:
         logger.warning(f"Auto-activation failed: {msg}")
         
    return None # Stop timer

def auto_activate_license():
    """
    Called by timer on startup. 
    Attempts to activate using the key stored in preferences.
    """
    try:
        # Get the root addon package name
        addon_name = __package__.split('.core')[0]
        prefs = bpy.context.preferences.addons.get(addon_name)
        if not prefs:
            return None
        
        pref_data = prefs.preferences
        key = pref_data.license_key

        if not key:
            return None

        # Start async validation
        logger.info(f"Auto-activating license: {key[:4]}...")
        validate_license_async(key)
        
        # Register a new separate timer for polling to be clean
        bpy.app.timers.register(_poll_activation_result)
        
        return None
    except Exception as e:
        logger.error(f"Error in auto_activate_license: {e}")
        return None
