"""UIList cho hiển thị danh sách textures trong converter popup"""

import bpy
from bpy.types import UIList


class SKLUM_UL_ConverterTextureList(UIList):
    """UIList hiển thị danh sách PNG textures để convert"""

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)

            # Checkbox enabled
            row.prop(item, "enabled", text="")

            # Image name
            row.label(text=item.image_name, icon='IMAGE_DATA')

            # Quality display
            if item.use_custom_quality:
                sub = row.row(align=True)
                sub.prop(item, "quality", text="")
                sub.prop(item, "use_custom_quality", text="", icon='PINNED')
            else:
                settings = context.scene.sklum_converter_settings
                row.label(text=f"{settings.global_quality}%")
                row.prop(item, "use_custom_quality", text="", icon='UNPINNED')

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.prop(item, "enabled", text="", icon='IMAGE_DATA')


classes = (SKLUM_UL_ConverterTextureList,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
