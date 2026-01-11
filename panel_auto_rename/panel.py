"""UI Panel cho SKLUM - Auto Rename"""

import bpy
from bpy.types import Panel

from . import utils


class VIEW3D_PT_sklum_auto_rename(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SKLUM Tools'
    bl_label = "SKLUM - Auto Rename"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        settings = context.scene.sklum_auto_rename_settings

        box = layout.box()
        box.label(text="Thông tin chung")

        row = box.row(align=True)
        row.prop(settings, "csv_filepath")
        row.operator("sklum.load_idp_csv", text="Nhập", icon='FILE_REFRESH')

        box.prop(settings, "model_id")

        row = box.row()
        row.prop(settings, "idp")

        utils.draw_preset_input(box, settings, "model_type", "model_types", "SKLUM_MT_model_type_presets")

        row = box.row()
        row.prop(settings, "main_material", text="Collection")

        box = layout.box()
        box.label(text="Các phần của mô hình")

        box.operator("sklum.auto_rename_add_item", icon='ADD')

        box.template_list(
            "SKLUM_UL_AutoRenameList",
            "",
            settings,
            "items",
            settings,
            "active_index",
            rows=3,
        )

        row = box.row(align=True)
        row.operator("sklum.auto_rename_remove_item", icon='REMOVE', text="Remove Selected")
        row.operator("sklum.auto_rename_clear_list", icon='TRASH', text="Clear All")

        if settings.items and settings.active_index < len(settings.items):
            item = settings.items[settings.active_index]

            item_box = box.box()
            utils.draw_preset_input(item_box, item, "mesh_name", "mesh_names", "SKLUM_MT_mesh_name_presets")
            utils.draw_preset_input(item_box, item, "material_name", "material_names", "SKLUM_MT_material_name_presets")

        layout.operator("sklum.auto_rename_execute", text="Đổi", icon='PLAY')


classes = (
    VIEW3D_PT_sklum_auto_rename,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
