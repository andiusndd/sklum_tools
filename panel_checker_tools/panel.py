"""Main panel: SKLUM - Checker & Tools"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_sklum_tools(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SKLUM Tools'
    bl_label = "SKLUM - Checker & Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("sklum.check_all", text="Check All / Refresh", icon='FILE_REFRESH')

        if scene.sklum_check_all_result:
            has_errors = any(
                line.strip().startswith("[LỖI]")
                for line in scene.sklum_check_all_result.split("\n")
            )

            header_box = layout.box()
            if has_errors:
                header_box.alert = True
            header_row = header_box.row()
            header_row.prop(
                scene,
                "sklum_check_all_collapsed",
                icon="TRIA_DOWN" if not scene.sklum_check_all_collapsed else "TRIA_RIGHT",
                icon_only=True,
                emboss=False,
            )
            header_row.label(text="📊 KẾT QUẢ TỔNG HỢP", icon='VIEWZOOM')

            summary_box = layout.box()
            if not scene.sklum_check_all_collapsed:
                for line in scene.sklum_check_all_result.split("\n"):
                    if not line.strip():
                        continue
                    sub_box = summary_box.box()
                    if line.strip().startswith("[LỖI]"):
                        sub_box.alert = True
                        sub_box.label(text=line, icon='ERROR')
                    elif line.strip().startswith("[OK]"):
                        sub_box.alert = False
                        sub_box.label(text=line, icon='CHECKMARK')
                    else:
                        sub_box.label(text=line)
            else:
                lines = [line.strip() for line in scene.sklum_check_all_result.split("\n") if line.strip()]
                error_count = sum(line.startswith("[LỖI]") for line in lines)
                ok_count = sum(line.startswith("[OK]") for line in lines)

                if error_count > 0:
                    error_box = summary_box.box()
                    error_box.alert = True
                    error_box.label(text=f"⚠️ {error_count} lỗi cần sửa", icon='ERROR')
                    if ok_count > 0:
                        ok_box = summary_box.box()
                        ok_box.alert = False
                        ok_box.label(text=f"✅ {ok_count} kiểm tra đạt chuẩn", icon='CHECKMARK')
                else:
                    ok_box = summary_box.box()
                    ok_box.alert = False
                    ok_box.label(text=f"✅ Tất cả {ok_count} kiểm tra đều đạt chuẩn", icon='CHECKMARK')

        layout.separator()

        # Rename section
        box = layout.box()
        row = box.row()
        row.prop(
            scene,
            "sklum_ui_rename_expand",
            icon="TRIA_DOWN" if scene.sklum_ui_rename_expand else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        row.label(text="Đổi Tên - Reset UVMap", icon='OUTLINER_DATA_FONT')
        if scene.sklum_ui_rename_expand:
            box.template_list("SKLUM_UL_rename_list", "", scene, "sklum_rename_list", scene, "sklum_rename_index")
            row = box.row(align=True)
            row.operator("sklum.refresh_rename_list", text="Refresh List", icon='FILE_REFRESH')
            row.operator("sklum.reset_uvmap", text="Reset UVMap Name", icon='UV')

        # Hard edges section
        box = layout.box()
        row = box.row()
        row.prop(
            scene,
            "sklum_ui_hard_edges_expand",
            icon="TRIA_DOWN" if scene.sklum_ui_hard_edges_expand else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        row.label(text="Kiểm Tra Cạnh Cứng", icon='MOD_BEVEL')
        if scene.sklum_ui_hard_edges_expand:
            row = box.row(align=True)
            row.prop(scene, "sklum_sharpness_angle", text="Angle")
            row.operator("sklum.select_hard_edges", text="Select Edges", icon='EDGESEL')

        # Color space section
        box = layout.box()
        row = box.row()
        row.prop(
            scene,
            "sklum_ui_color_space_expand",
            icon="TRIA_DOWN" if scene.sklum_ui_color_space_expand else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        row.label(text="Color Space - Convert .PNG", icon='IMAGE_RGB')
        if scene.sklum_ui_color_space_expand:
            box.template_list("SKLUM_UL_color_space_list", "", scene, "sklum_color_space_list", scene, "sklum_color_space_index")
            box.label(text="Standard: Base Color → sRGB, Others → Non-Color")
            row = box.row(align=True)
            row.operator("sklum.check_color_space", text="Check", icon='VIEWZOOM')
            if scene.sklum_color_space_needs_fix:
                row.operator("sklum.fix_color_space", text="Fix All", icon='ERROR')
            if scene.sklum_color_space_check_result:
                result_box = box.box()
                result_box.label(text=scene.sklum_color_space_check_result, icon='INFO')

        # Active point section
        box = layout.box()
        row = box.row()
        row.prop(
            scene,
            "sklum_ui_active_point_expand",
            icon="TRIA_DOWN" if scene.sklum_ui_active_point_expand else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        row.label(text="Active Point - Tạo Empty", icon='PIVOT_CURSOR')
        if scene.sklum_ui_active_point_expand:
            box.template_list(
                "SKLUM_UL_active_point_list",
                "",
                scene,
                "sklum_active_point_list",
                scene,
                "sklum_active_point_index",
                rows=2,
            )
            box.label(text="Standard: Origin at Center (X, Y) and Z=0")
            row = box.row(align=True)
            row.operator("sklum.check_active_point", text="Check", icon='VIEWZOOM')
            if scene.sklum_active_point_needs_fix:
                row.operator("sklum.fix_active_point", text="Fix All", icon='MODIFIER')
            else:
                box.operator("sklum.group_objects", text="Group to Origin", icon='OUTLINER_OB_EMPTY')
            box.operator("sklum.apply_transforms", text="Apply Rotate & Scale", icon='FILE_REFRESH')
            if scene.sklum_active_point_check_result:
                result_box = box.box()
                result_box.label(text=scene.sklum_active_point_check_result, icon='INFO')

        # Seam & sharp section
        box = layout.box()
        row = box.row()
        row.prop(
            scene,
            "sklum_ui_seam_sharp_expand",
            icon="TRIA_DOWN" if scene.sklum_ui_seam_sharp_expand else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        row.label(text="Seam - Sharp Edges", icon='UV')
        if scene.sklum_ui_seam_sharp_expand:
            box.template_list("SKLUM_UL_seam_list", "", scene, "sklum_seam_list", scene, "sklum_seam_index", rows=2)
            row = box.row(align=True)
            row.operator("sklum.check_seam", text="Check Seam", icon='VIEWZOOM')
            if scene.sklum_seam_needs_mark:
                row.operator("sklum.mark_seam_from_uv", text="Mark from UV", icon='MOD_UVPROJECT')
            if scene.sklum_seam_check_result:
                result_box = box.box()
                result_box.label(text=scene.sklum_seam_check_result, icon='INFO')
            row2 = box.row(align=True)
            row2.operator("sklum.convert_sharp_to_seam", text="Sharp to Seam", icon='MOD_EDGESPLIT')
            row2.operator("sklum.clear_seam", text="Clear Seam", icon='X')
            row2.operator("sklum.clear_sharp_edges", text="Clear Sharp", icon='MOD_SMOOTH')

        # Grid checker section
        box = layout.box()
        row = box.row()
        row.prop(
            scene,
            "sklum_ui_grid3_expand",
            icon="TRIA_DOWN" if scene.sklum_ui_grid3_expand else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        row.label(text="Kiểm Tra Số Lưới", icon='MESH_GRID')
        if scene.sklum_ui_grid3_expand:
            box.template_list("SKLUM_UL_grid3_list", "", scene, "sklum_grid3_list", scene, "sklum_grid3_index", rows=2)
            row = box.row(align=True)
            row.prop(scene, "sklum_grid3_mode", text="Chế độ")
            row.operator("sklum.check_grid3", text="Check", icon='VIEWZOOM').mode = scene.sklum_grid3_mode
            if scene.sklum_grid3_check_result:
                result_box = box.box()
                result_box.label(text=scene.sklum_grid3_check_result, icon='INFO')


classes = (VIEW3D_PT_sklum_tools,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
