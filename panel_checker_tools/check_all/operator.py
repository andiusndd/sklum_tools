"""Check All operator"""

import bpy
from bpy.types import Operator


class SKLUM_OT_check_all(Operator):
    """Run all available checks"""
    bl_idname = "sklum.check_all"
    bl_label = "Check All / Refresh"
    bl_description = "Run all checks (Seam, Color Space, Active Point, etc.)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # This operator can always run
        return True

    def execute(self, context):
        # Call all individual check operators sequentially using hasattr for safety
        if hasattr(bpy.ops.sklum, 'check_seam'):
            bpy.ops.sklum.check_seam('EXEC_DEFAULT')
        
        if hasattr(bpy.ops.sklum, 'check_color_space'):
            bpy.ops.sklum.check_color_space('EXEC_DEFAULT')
            
        if hasattr(bpy.ops.sklum, 'check_active_point'):
            bpy.ops.sklum.check_active_point('EXEC_DEFAULT')
            
        if hasattr(bpy.ops.sklum, 'refresh_rename_list'):
            bpy.ops.sklum.refresh_rename_list('EXEC_DEFAULT')

        # Gọi check_grid3 với mode triangle (tam giác)
        if hasattr(bpy.ops.sklum, 'check_grid3'):
            bpy.ops.sklum.check_grid3('EXEC_DEFAULT', mode='TRIANGLE')

        scene = context.scene

        # Kiểm tra UVMap: mỗi object chỉ có 1 UVMap và tên phải là 'UVMap'
        uvmap_errors = []
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                uv_layers = obj.data.uv_layers
                if len(uv_layers) != 1:
                    uvmap_errors.append(f"{obj.name}: Có {len(uv_layers)} UVMap")
                elif uv_layers[0].name != 'UVMap':
                    uvmap_errors.append(f"{obj.name}: Tên UVMap là '{uv_layers[0].name}'")
        if not context.selected_objects:
            scene.sklum_uvmap_check_result = "Chưa chọn vật nào để kiểm tra."
        elif uvmap_errors:
            scene.sklum_uvmap_check_result = "Phát hiện lỗi UVMap:\n" + "\n".join(uvmap_errors)
        else:
            scene.sklum_uvmap_check_result = "Tất cả object đều có đúng 1 UVMap tên 'UVMap'."

        # Kiểm tra UV outside [0,1]
        uv_outside_errors = []
        for obj in context.selected_objects:
            if obj.type == 'MESH' and obj.data.uv_layers:
                uv_layer = obj.data.uv_layers.active.data
                for i, loop in enumerate(uv_layer):
                    u, v = loop.uv
                    if u < 0 or u > 1 or v < 0 or v > 1:
                        uv_outside_errors.append(f"{obj.name}: UV ngoài [0,1] tại index {i} ({u:.3f}, {v:.3f})")
                        break
        if not context.selected_objects:
            scene.sklum_uv_outside_check_result = "Chưa chọn vật nào để kiểm tra."
        elif uv_outside_errors:
            scene.sklum_uv_outside_check_result = "Phát hiện UV outside:\n" + "\n".join(uv_outside_errors)
        else:
            scene.sklum_uv_outside_check_result = "Tất cả UV đều nằm trong [0,1]."

        # Kiểm tra texture pack: mỗi image của node TEX_IMAGE trong vật liệu phải được pack
        texture_pack_errors = []
        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image:
                    if not node.image.packed_file:
                        texture_pack_errors.append(f"{mat.name}: {node.image.name} chưa được pack")
        if not bpy.data.materials:
            scene.sklum_texture_pack_check_result = "Không có material nào để kiểm tra."
        elif texture_pack_errors:
            scene.sklum_texture_pack_check_result = "Phát hiện texture chưa pack:\n" + "\n".join(texture_pack_errors)
        else:
            scene.sklum_texture_pack_check_result = "Tất cả texture đã được pack."

        # Kiểm tra cạnh mark sharp hoặc mean crease
        edge_sharp_crease_errors = []
        checked = False
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                checked = True
                for edge in obj.data.edges:
                    if getattr(edge, 'use_edge_sharp', False) or getattr(edge, 'crease', 0) > 0:
                        edge_sharp_crease_errors.append(f"{obj.name}: Có cạnh mark sharp hoặc mean crease (edge index {edge.index})")
                        break
        if not checked:
            scene.sklum_edge_sharp_crease_check_result = "[LỖI] Edge Sharp/Crease: Chưa chọn vật nào để kiểm tra."
        elif edge_sharp_crease_errors:
            scene.sklum_edge_sharp_crease_check_result = "[LỖI] Edge Sharp/Crease: Phát hiện cạnh mark sharp hoặc mean crease:\n" + "\n".join(edge_sharp_crease_errors)
        else:
            scene.sklum_edge_sharp_crease_check_result = "[OK] Edge Sharp/Crease: Không có cạnh nào mark sharp hoặc mean crease."

        # Kiểm tra vertex groups: không được có vertex group
        vertex_group_errors = []
        for obj in context.selected_objects:
            if obj.type == 'MESH' and obj.vertex_groups:
                vertex_group_errors.append(f"{obj.name}: Có {len(obj.vertex_groups)} vertex group")
        if not context.selected_objects:
            scene.sklum_vertex_group_check_result = "Chưa chọn vật nào để kiểm tra."
        elif vertex_group_errors:
            scene.sklum_vertex_group_check_result = "Phát hiện object có vertex group:\n" + "\n".join(vertex_group_errors)
        else:
            scene.sklum_vertex_group_check_result = "Không có object nào có vertex group."

        # Kiểm tra modifier: không được có modifier
        modifier_errors = []
        for obj in context.selected_objects:
            if obj.type == 'MESH' and obj.modifiers:
                modifier_errors.append(f"{obj.name}: Có {len(obj.modifiers)} modifier")
        if not context.selected_objects:
            scene.sklum_modifier_check_result = "Chưa chọn vật nào để kiểm tra."
        elif modifier_errors:
            scene.sklum_modifier_check_result = "Phát hiện object có modifier:\n" + "\n".join(modifier_errors)
        else:
            scene.sklum_modifier_check_result = "Không có object nào có modifier."

        # Tổng hợp kết quả
        result_lines = []
        check_fields = [
            ('Seam', 'sklum_seam_check_result'),
            ('Color Space', 'sklum_color_space_check_result'),
            ('Active Point', 'sklum_active_point_check_result'),
            ('Triangle', 'sklum_grid3_check_result'),
            ('UVMap', 'sklum_uvmap_check_result'),
            ('UV Outside', 'sklum_uv_outside_check_result'),
            ('Texture Pack', 'sklum_texture_pack_check_result'),
            ('Edge Sharp/Crease', 'sklum_edge_sharp_crease_check_result'),
            ('Vertex Group', 'sklum_vertex_group_check_result'),
            ('Modifier', 'sklum_modifier_check_result'),
        ]
        for label, attr in check_fields:
            if hasattr(scene, attr):
                msg = getattr(scene, attr)
                if msg.startswith('[OK]') or msg.startswith('[LỖI]'):
                    if "buffet:" not in msg.lower():
                        result_lines.append(msg)
                else:
                    ok = False
                    lower_msg = msg.lower()
                    if label == 'Triangle':
                        ok = "không tìm thấy mặt tam giác nào" in lower_msg or "không tìm thấy mặt n-gon nào" in lower_msg
                    elif label == 'Edge Sharp/Crease':
                        ok = "không có cạnh nào mark sharp" in lower_msg or "không có cạnh nào" in lower_msg
                    elif label == 'Vertex Group':
                        ok = "không có object nào có vertex group" in lower_msg or "không có vertex group" in lower_msg
                    elif label == 'Modifier':
                        ok = "không có object nào có modifier" in lower_msg or "không có modifier" in lower_msg
                    elif label == 'UVMap':
                        ok = "tất cả" in lower_msg or "đều có đúng" in lower_msg
                    elif label == 'UV Outside':
                        ok = "tất cả" in lower_msg or "đều nằm trong" in lower_msg
                    elif label == 'Texture Pack':
                        ok = "tất cả" in lower_msg or "đã được pack" in lower_msg
                    else:
                        ok = "tất cả" in lower_msg or "đều đúng" in lower_msg
                    if ok:
                        result_lines.append(f"[OK] {label}: {msg}")
                    else:
                        result_lines.append(f"[LỖI] {label}: {msg}")

        scene.sklum_check_all_result = "\n".join(result_lines)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(SKLUM_OT_check_all)


def unregister():
    bpy.utils.unregister_class(SKLUM_OT_check_all)
