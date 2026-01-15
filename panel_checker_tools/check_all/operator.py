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
        scene = context.scene
        sklum = scene.sklum
        wm = context.window_manager

        # LICENSE CHECK
        if not sklum.license_active:
             self.report({'ERROR'}, "Vui lòng kích hoạt License để sử dụng.")
             return {'CANCELLED'}

        # START PROGRESS BAR
        total_steps = 11  # Number of checks being run
        wm.progress_begin(0, total_steps)
        current_step = 0

        try:
            # 1. Seam Check
            current_step += 1
            wm.progress_update(current_step)
            if hasattr(bpy.ops.sklum, 'check_seam'):
                bpy.ops.sklum.check_seam('EXEC_DEFAULT')
            
            # 2. Color Space Check
            current_step += 1
            wm.progress_update(current_step)
            if hasattr(bpy.ops.sklum, 'check_color_space'):
                bpy.ops.sklum.check_color_space('EXEC_DEFAULT')
                
            # 3. Active Point Check
            current_step += 1
            wm.progress_update(current_step)
            if hasattr(bpy.ops.sklum, 'check_active_point'):
                bpy.ops.sklum.check_active_point('EXEC_DEFAULT')
                
            # 4. Refresh Rename List
            current_step += 1
            wm.progress_update(current_step)
            if hasattr(bpy.ops.sklum, 'refresh_rename_list'):
                bpy.ops.sklum.refresh_rename_list('EXEC_DEFAULT')

            # 5. Grid Check
            current_step += 1
            wm.progress_update(current_step)
            if hasattr(bpy.ops.sklum, 'check_grid3'):
                bpy.ops.sklum.check_grid3('EXEC_DEFAULT', mode='TRIANGLE')

            # --- CORE LOGIC CHECKS ---
            sklum.check_results_data.clear()
            
            def add_result(label, res):
                item = sklum.check_results_data.add()
                item.label = label
                item.status = res.status
                item.message = res.message
                item.failed_count = len(res.failed_objects) if res.failed_objects else 0
                return item

            selected = context.selected_objects

            # 6. UVMap
            current_step += 1
            wm.progress_update(current_step)
            add_result("UVMap", checker_logic.check_uv_map(selected))
            
            # 7. UV Outside
            current_step += 1
            wm.progress_update(current_step)
            add_result("UV Outside", checker_logic.check_uv_outside(selected))
            
            # 8. Texture Pack
            current_step += 1
            wm.progress_update(current_step)
            add_result("Texture Pack", checker_logic.check_texture_pack(bpy.data.materials))
            
            # 9. Edge Sharp/Crease
            current_step += 1
            wm.progress_update(current_step)
            add_result("Edge Sharp/Crease", checker_logic.check_edge_sharp_crease(selected))
            
            # 10. Vertex Groups
            current_step += 1
            wm.progress_update(current_step)
            add_result("Vertex Group", checker_logic.check_vertex_groups(selected))
            
            # 11. Modifiers
            current_step += 1
            wm.progress_update(current_step)
            add_result("Modifier", checker_logic.check_modifiers(selected))

        finally:
            wm.progress_end()

        # Generate summary string
        result_lines = []
        legacy_checks = [
            ('Seam', 'seam_check_result'),
            ('Color Space', 'color_space_check_result'),
            ('Active Point', 'active_point_check_result'),
            ('Triangle', 'grid3_check_result'),
        ]
        
        for label, attr in legacy_checks:
            if hasattr(sklum, attr):
                msg = getattr(sklum, attr)
                if msg:
                     result_lines.append(msg)

        sklum.check_all_result = "\n".join(result_lines)
        self.report({'INFO'}, "All checks completed.")

        return {'FINISHED'}


def register():
    bpy.utils.register_class(SKLUM_OT_check_all)


def unregister():
    bpy.utils.unregister_class(SKLUM_OT_check_all)
