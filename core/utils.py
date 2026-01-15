"""
Utils - Các hàm tiện ích dùng chung
"""

import bpy
import math
import os
import requests
import zipfile
import shutil
import tempfile
import time
from .constants import ORIGIN_TOLERANCE

def get_selected_meshes(context):
    """Lấy danh sách các mesh objects đang được chọn"""
    return [obj for obj in context.selected_objects if obj.type == 'MESH']


def is_origin_at_center(obj, tolerance=ORIGIN_TOLERANCE):
    """
    Kiểm tra xem origin của object có ở tâm không
    Returns: (is_centered, message)
    """
    loc = obj.location
    x_ok = abs(loc.x) < tolerance
    y_ok = abs(loc.y) < tolerance
    z_ok = abs(loc.z) < tolerance
    
    if x_ok and y_ok and z_ok:
        return True, "OK"
    else:
        return False, f"X={loc.x:.4f}, Y={loc.y:.4f}, Z={loc.z:.4f}"


def get_material_textures(material):
    """
    Lấy tất cả các texture nodes từ material
    Returns: list of (node, image) tuples
    """
    textures = []
    if material and material.use_nodes:
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                textures.append((node, node.image))
    return textures


def is_base_color_texture(node_name):
    """Kiểm tra xem texture có phải là Base Color không dựa vào tên"""
    from .constants import BASE_COLOR_KEYWORDS
    name_lower = node_name.lower()
    return any(keyword in name_lower for keyword in BASE_COLOR_KEYWORDS)


def show_message_box(message="", title="Message", icon='INFO'):
    """Hiển thị message box"""
    def draw(self, context):
        self.layout.label(text=message)
    
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def format_check_result(is_ok, ok_message, error_message):
    """
    Format kết quả kiểm tra với prefix [OK] hoặc [LỖI]
    """
    if is_ok:
        return f"[OK] {ok_message}"
    else:
        return f"[LỖI] {error_message}"


def safe_mode_set(mode):
    """Chuyển mode an toàn, chỉ khi có object được chọn"""
    if bpy.context.selected_objects:
        bpy.ops.object.mode_set(mode=mode)


def check_for_update(repo_url):
    """
    Kiểm tra phiên bản mới từ GitHub.
    Returns: (is_update_available, latest_version_str, error_msg)
    """
    try:
        from .logger import logger
        # Clean URL construction
        if repo_url.endswith(".git"):
            base_url = repo_url[:-4]
        else:
            base_url = repo_url
            
        # Use raw.githubusercontent.com for manifest
        raw_base = base_url.replace("https://github.com/", "https://raw.githubusercontent.com/")
        manifest_url = f"{raw_base}/main/blender_manifest.toml"
        
        logger.info(f"Checking updates from {manifest_url}")
        response = requests.get(manifest_url, timeout=10)
        response.raise_for_status()
        
        import tomllib
        manifest_data = tomllib.loads(response.text)
        remote_version_str = manifest_data.get("version", "0.0.0")
        
        # Get local version from manifest
        addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        local_manifest_path = os.path.join(addon_dir, "blender_manifest.toml")
        with open(local_manifest_path, "rb") as f:
            local_manifest_data = tomllib.load(f)
        local_version_str = local_manifest_data.get("version", "0.0.0")
        
        if remote_version_str != local_version_str:
            logger.info(f"New version found: {remote_version_str} (Local: {local_version_str})")
            return True, remote_version_str, None
        
        logger.info("Addon is up to date.")
        return False, local_version_str, None
        
    except Exception as e:
        from .logger import logger
        logger.error(f"Error checking for updates: {e}")
        return False, None, str(e)


def safe_remove(path, max_attempts=5, delay=0.5):
    """
    Thử xóa file nhiều lần với khoảng trễ để tránh WinError 32 trên Windows.
    """
    from .logger import logger
    for i in range(max_attempts):
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            return True
        except Exception as e:
            logger.warning(f"Delete attempt {i+1} failed for {path}: {e}")
            time.sleep(delay)
    return False


def download_and_install_update(repo_url):
    """
    Tải về và cài đặt bản cập nhật từ GitHub sử dụng chiến lược 'Rename-Swap'.
    """
    from .logger import logger
    try:
        # Clean URL construction
        if repo_url.endswith(".git"):
            base_url = repo_url[:-4]
        else:
            base_url = repo_url
            
        tmp_path = None
        temp_extract_dir = None
        
        try:
            zip_url = f"{base_url}/archive/refs/heads/main.zip"
            logger.info(f"Downloading update from {zip_url}")
            
            response = requests.get(zip_url, stream=True, timeout=30)
            response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp_file.write(chunk)
                tmp_path = tmp_file.name
                
            # Current addon directory (e.g., .../scripts/addons/SKLUMToolz)
            addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            addon_parent = os.path.dirname(addon_dir)
            addon_folder_name = os.path.basename(addon_dir)
            
            logger.info(f"Extracting to temporary directory...")
            with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                temp_extract_dir = tempfile.mkdtemp()
                zip_ref.extractall(temp_extract_dir)
                
                extracted_folders = os.listdir(temp_extract_dir)
                if not extracted_folders:
                    raise Exception("Zip file is empty")
                
                source_dir = os.path.join(temp_extract_dir, extracted_folders[0])
                
                # --- START ATOMIC SWAP ---
                # 1. Prepare old directory path
                timestamp = int(time.time())
                old_dir = os.path.join(addon_parent, f"{addon_folder_name}_old_{timestamp}")
                
                logger.info(f"Swapping directories...")
                
                # CRITICAL: Force close logger handlers to release locks on current folder
                try:
                    logger.shutdown()
                except Exception as log_e:
                    print(f"Update: Error shutting down logger: {log_e}")

                # 2. Rename current to old (Retry loop)
                renamed = False
                for i in range(10):
                    try:
                        os.rename(addon_dir, old_dir)
                        renamed = True
                        break
                    except OSError as e:
                        # WinError 5 or 32
                        time.sleep(0.5)
                        # Try to gc collect to release handles?
                        import gc
                        gc.collect()
                
                if not renamed:
                     # Re-init logger to report error if we failed
                     # But shutdown killed instance? No, just handlers.
                     # We can just return error.
                     return False, f"Could not rename addon folder (Access Denied). Please restart Blender and try again."

                try:
                    # 3. Move new directory to current path
                    shutil.move(source_dir, addon_dir)
                    
                    # 4. Success! Try to cleanup the old dir
                    if safe_remove(old_dir):
                        print("Update: Cleanup successful.")
                    else:
                        print(f"Update: Could not delete old version at {old_dir}. It will be cleaned up next time or manually.")
                        
                except Exception as e:
                    # Rollback: Try to move old back to current if swap failed
                    print(f"Installation failed, attempting rollback: {e}")
                    if os.path.exists(old_dir) and not os.path.exists(addon_dir):
                        try:
                            os.rename(old_dir, addon_dir)
                        except:
                            pass
                    raise e
                
            return True, "Update installed successfully. Please restart Blender."
            
        finally:
            # Cleanup temp files
            if temp_extract_dir and os.path.exists(temp_extract_dir):
                safe_remove(temp_extract_dir)
            if tmp_path and os.path.exists(tmp_path):
                safe_remove(tmp_path)
        
    except Exception as e:
        logger.error(f"Update failed: {e}")
        return False, str(e)
