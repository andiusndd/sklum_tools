"""
Global Storage - Manages persistent data in User Home directory
Path: ~/.sklum_tools/config.json
"""
import os
import json
from pathlib import Path

def get_config_dir():
    """Returns the persistent config directory path."""
    home = Path.home()
    config_dir = home / ".sklum_tools"
    if not config_dir.exists():
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
            # Hide folder on Windows
            if os.name == 'nt':
                import ctypes
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ctypes.windll.kernel32.SetFileAttributesW(str(config_dir), FILE_ATTRIBUTE_HIDDEN)
        except Exception as e:
            print(f"SKLUM Tools: Failed to create config dir: {e}")
            return None
    return config_dir

def get_config_file():
    """Returns the path to config.json."""
    config_dir = get_config_dir()
    if config_dir:
        return config_dir / "config.json"
    return None

def save_license_key_global(key):
    """Saves the license key to the global config file."""
    if not key:
        return # Don't save empty keys if not necessary, or should we allow clearing?
               # Let's allow clearing if key is empty string.
    
    file_path = get_config_file()
    if not file_path:
        return

    data = {}
    # Load existing data to preserve other future settings
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            pass # corrupted or empty

    data["license_key"] = key

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"SKLUM Tools: Failed to save global license: {e}")

def load_license_key_global():
    """Loads the license key from the global config file."""
    file_path = get_config_file()
    if not file_path or not file_path.exists():
        return ""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("license_key", "")
    except Exception as e:
        print(f"SKLUM Tools: Failed to load global license: {e}")
        return ""
