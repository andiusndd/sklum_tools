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
        # Clean URL construction
        if repo_url.endswith(".git"):
            base_url = repo_url[:-4]
        else:
            base_url = repo_url
            
        # Use raw.githubusercontent.com for manifest
        raw_base = base_url.replace("https://github.com/", "https://raw.githubusercontent.com/")
        manifest_url = f"{raw_base}/main/blender_manifest.toml"
        
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
        
        # Simple string comparison or tuple comparison if formatted correctly
        if remote_version_str != local_version_str:
            return True, remote_version_str, None
        return False, local_version_str, None
        
    except Exception as e:
        return False, None, str(e)


def download_and_install_update(repo_url):
    """
    Tải về và cài đặt bản cập nhật từ GitHub.
    """
    try:
        # Clean URL construction
        if repo_url.endswith(".git"):
            base_url = repo_url[:-4]
        else:
            base_url = repo_url
            
        zip_url = f"{base_url}/archive/refs/heads/main.zip"
        
        response = requests.get(zip_url, stream=True, timeout=30)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            tmp_path = tmp_file.name
            
        # Get addon directory
        addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        parent_dir = os.path.dirname(addon_dir)
        addon_name = os.path.basename(addon_dir)
        
        with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
            # Extract to a temp directory first
            temp_extract_dir = tempfile.mkdtemp()
            zip_ref.extractall(temp_extract_dir)
            
            # The zip usually contains a folder named "repo_name-main"
            extracted_folders = os.listdir(temp_extract_dir)
            if not extracted_folders:
                raise Exception("Zip file is empty")
            
            source_dir = os.path.join(temp_extract_dir, extracted_folders[0])
            
            # Replace files in the current addon directory
            # WARNING: This is destructive to the current session until restart
            for item in os.listdir(source_dir):
                s = os.path.join(source_dir, item)
                d = os.path.join(addon_dir, item)
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            
            # Cleanup temp extract dir (source files)
            shutil.rmtree(temp_extract_dir)
            
        # Cleanup the downloaded ZIP file after closing zipfile handle
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            
        return True, "Update installed successfully. Please restart Blender."
        
    except Exception as e:
        return False, str(e)
