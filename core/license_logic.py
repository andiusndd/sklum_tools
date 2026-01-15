import subprocess
import requests
import sys

def get_machine_id():
    """Gets a unique ID for the machine (Windows UUID)."""
    try:
        # standard windows command to get motherboard uuid
        cmd = "wmic csproduct get uuid"
        uuid = subprocess.check_output(cmd, shell=True).decode().split('\n')[1].strip()
        if not uuid:
            return "UNKNOWN_HWID"
        return uuid
    except:
        return "UNKNOWN_HWID_ERROR"

def validate_license(key):
    """
    Validates the license key against the server.
    MOCKED FOR PHASE 1: Returns True if key > 5 chars.
    """
    if not key:
        return False, "Vui lòng nhập License Key."
        
    # Mock validation
    # Real logic: POST to https://my-vercel-api.com/api/activate
    # with json={'key': key, 'hwid': get_machine_id()}
    
    if len(key) > 5:
        # Mocking success
        # In real world, logic is here.
        return True, "Kích hoạt thành công (Mock)."
    else:
        return False, "Key không hợp lệ (Mock > 5 chars)."
