"""UI list cho Auto Rename"""

import bpy
from bpy.types import UIList


class SKLUM_UL_AutoRenameList(UIList):
    """Danh sách các phần của mô hình cần đổi tên"""

    bl_idname = "SKLUM_UL_AutoRenameList"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            split = layout.split(factor=0.9)
            split.label(text=item.mesh_name, icon='OBJECT_DATA')
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


classes = (
    SKLUM_UL_AutoRenameList,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
