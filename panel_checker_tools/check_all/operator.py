"""Check All operator"""

import bpy
from bpy.types import Operator
from ...core import checker_logic


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
        # LICENSE CHECK
        if not context.scene.sklum_license_active:
             self.report({'ERROR'}, "Vui lòng kích hoạt License để sử dụng.")
             return {'CANCELLED'}

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
        
        # Clear previous results
        scene.sklum_check_results_data.clear()
        
        def add_result(label, res):
            item = scene.sklum_check_results_data.add()
            item.label = label
            item.status = res.status
            item.message = res.message
            item.failed_count = len(res.failed_objects) if res.failed_objects else 0
            
            # Legacy string support (temporary, can remove if UI is fully updated)
            # We keep it empty or simple to avoid errors if UI still references it
            return item

        # Check UVMap
        add_result("UVMap", checker_logic.check_uv_map(context.selected_objects))
        
        # Check UV Outside
        add_result("UV Outside", checker_logic.check_uv_outside(context.selected_objects))
        
        # Check Texture Pack
        add_result("Texture Pack", checker_logic.check_texture_pack(bpy.data.materials))
        
        # Check Edge Sharp/Crease
        add_result("Edge Sharp/Crease", checker_logic.check_edge_sharp_crease(context.selected_objects))
        
        # Check Vertex Groups
        add_result("Vertex Group", checker_logic.check_vertex_groups(context.selected_objects))
        
        # Check Modifiers
        add_result("Modifier", checker_logic.check_modifiers(context.selected_objects))

        # Generate summary string from structured data
        result_lines = []
        
        # Add other checks (legacy ones that are not yet migrated to new system if any)
        # For now, we assume all critical checks are in sklum_check_results_data
        # But wait, 'Seam', 'Color Space', 'Active Point', 'Triangle' are executed via OTHER operators.
        # Those operators might still set their respective string properties.
        # So we should still read them if they exist.
        
        legacy_checks = [
            ('Seam', 'sklum_seam_check_result'),
            ('Color Space', 'sklum_color_space_check_result'),
            ('Active Point', 'sklum_active_point_check_result'),
            ('Triangle', 'sklum_grid3_check_result'),
        ]
        
        for label, attr in legacy_checks:
            if hasattr(scene, attr):
                msg = getattr(scene, attr)
                if msg:
                     # Simple heuristics since we haven't refactored these yet
                     if "[LỖI]" in msg or ("không" not in msg.lower() and "đúng" not in msg.lower() and "ok" not in msg.lower()):
                         # This heuristic is weak, but keeps existing behavior for now
                         if msg.startswith("[OK]") or msg.startswith("[LỖI]"):
                             result_lines.append(msg)
                         else:
                             # Try to format it
                             # But sticking to original string is safer if we don't know format
                             result_lines.append(msg)

        scene.sklum_check_all_result = "\n".join(result_lines)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(SKLUM_OT_check_all)


def unregister():
    bpy.utils.unregister_class(SKLUM_OT_check_all)
