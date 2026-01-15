"""UI Panel cho SKLUM - JPG Converter"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_sklum_jpg_converter(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SKLUM Tools'
    bl_label = "SKLUM - JPG Converter"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        """Only show this panel if license is active"""
        return context.scene.sklum_license_active

    def draw(self, context):
        layout = self.layout

        # Main button - open popup
        box = layout.box()
        box.label(text="Chuyển đổi PNG sang JPG", icon='FILE_IMAGE')

        row = box.row()
        row.scale_y = 1.5
        row.operator("sklum.open_converter_popup", text="Convert PNG to JPG", icon='IMAGE_RGB')

        box.label(text="Mở popup với danh sách textures và settings.", icon='INFO')

        layout.separator()

        # Quick convert buttons (optional shortcuts)
        box = layout.box()
        row = box.row()
        row.prop(
            context.scene,
            "sklum_show_quick_convert",
            icon="TRIA_DOWN" if context.scene.get("sklum_show_quick_convert") else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        row.label(text="Quick Convert (Tất cả PNG)", icon='FORCE_CHARGE')

        if context.scene.get("sklum_show_quick_convert"):
            row_opts = box.row(align=True)
            op95 = row_opts.operator("sklum.convert_png_to_jpg_quality", text="95%")
            op95.quality = 95

            op65 = row_opts.operator("sklum.convert_png_to_jpg_quality", text="65%")
            op65.quality = 65

            op35 = row_opts.operator("sklum.convert_png_to_jpg_quality", text="35%")
            op35.quality = 35

            box.label(text="Áp dụng cho tất cả PNG đã unpack.", icon='INFO')


classes = (VIEW3D_PT_sklum_jpg_converter,)


def register():
    # Property for collapsible section
    bpy.types.Scene.sklum_show_quick_convert = bpy.props.BoolProperty(default=False)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    if hasattr(bpy.types.Scene, 'sklum_show_quick_convert'):
        del bpy.types.Scene.sklum_show_quick_convert
