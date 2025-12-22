"""
Utils - Các hàm tiện ích dùng chung
"""

import bpy
import math
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
