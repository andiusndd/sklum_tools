import subprocess
import requests
import sys

# Replace this with your actual Vercel URL
API_URL = "https://sklum-license-backend.vercel.app/api/index"

def get_machine_id():
    """Gets a unique ID for the machine (Windows UUID)."""
    # Method 1: WMIC (Standard)
    try:
        cmd = "wmic csproduct get uuid"
        output = subprocess.check_output(cmd, shell=True).decode()
        # Parse output carefully
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1:
            return lines[1]
    except:
        pass

    # Method 2: PowerShell (Modern Windows)
    try:
        cmd = 'powershell "Get-CimInstance -Class Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"'
        uuid = subprocess.check_output(cmd, shell=True).decode().strip()
        if uuid:
            return uuid
    except:
        pass
        
    # Method 3: MAC Address (Fallback)
    try:
        import uuid
        return str(uuid.getnode())
    except:
        pass

    return "UNKNOWN_HWID_ERROR"

def validate_license(key):
    """
    Validates the license key against the server.
    """
    if not key:
        return False, "Vui lòng nhập License Key."
    
    hwid = get_machine_id()
    payload = {
        'key': key.strip(),
        'hwid': hwid
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        
        # Check HTTP Status Code
        if response.status_code == 200:
            data = response.json()
            return True, data.get('message', "License Valid")
        else:
            # 403, 404, 500
            try:
                data = response.json()
                msg = data.get('message', f"Error {response.status_code}")
                return False, msg
            except:
                return False, f"Server Error {response.status_code}"
                
    except requests.exceptions.Timeout:
        return False, "Hết thời gian kết nối (Timeout). Vui lòng kiểm tra mạng."
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối đến Server. Vui lòng kiểm tra mạng."
    except Exception as e:
        return False, f"Lỗi không xác định: {str(e)}"
