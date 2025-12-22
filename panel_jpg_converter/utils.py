"""Utilities cho panel JPG Converter"""

import sys
import subprocess


_pillow_installed = False


def ensure_pillow_is_installed():
    """Đảm bảo thư viện Pillow đã sẵn sàng sử dụng."""
    global _pillow_installed
    if _pillow_installed:
        return True, ""

    try:
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--user"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "--user"])

        import site
        user_site_packages = site.getusersitepackages()
        if user_site_packages not in sys.path:
            sys.path.append(user_site_packages)

        from PIL import Image  # noqa: F401  # Kiểm tra import
        _pillow_installed = True
        return True, "Pillow was installed successfully."
    except Exception as exc:
        return False, f"Failed to install Pillow: {exc}"


def register():
    """Module utils không có gì để đăng ký."""


def unregister():
    """Module utils không có gì để hủy đăng ký."""
