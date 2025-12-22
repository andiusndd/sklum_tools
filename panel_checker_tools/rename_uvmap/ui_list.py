"""UI List cho danh sách đổi tên"""

import bpy
from bpy.types import UIList


class SKLUM_UL_rename_list(UIList):
    """Danh sách các mục có thể đổi tên"""

    bl_idname = "SKLUM_UL_rename_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if not item.is_renaming:
            split = layout.split(factor=0.2)
            split.label(text=item.obj_type.title())

            split = split.split(factor=0.4)
            split.label(text=item.obj_name)

            split = split.split(factor=0.5)
            split.label(text=item.mat_name if item.obj_type in {'MATERIAL', 'IMAGE'} else "-")

            op = split.operator("sklum.rename_start", text="Rename", icon='GREASEPENCIL')
            op.index = index
        else:
            split = layout.split(factor=0.7)
            split.prop(item, "new_name", text="")

            row = split.row(align=True)
            op_ok = row.operator("sklum.rename_confirm", text="OK", icon='CHECKMARK')
            op_ok.index = index
            row.operator("sklum.refresh_rename_list", text="", icon='CANCEL')


classes = (SKLUM_UL_rename_list,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
