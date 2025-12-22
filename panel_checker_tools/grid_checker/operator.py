"""Operator for Grid Checker section"""

import bpy
import bmesh
from bpy.types import Operator, PropertyGroup, UIList
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    EnumProperty,
    CollectionProperty,
)


class SKLUM_MT_grid3_entry(PropertyGroup):
    obj_name: StringProperty(name="Tên Vật")
    face_count: IntProperty(name="Số Lưới")
    is_grid3: BoolProperty(name="Có đúng 3 lưới")


class SKLUM_UL_grid3_list(UIList):
    bl_idname = "SKLUM_UL_grid3_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.6)
        split.label(text=item.obj_name)
        split.label(text=str(item.face_count))
        split.label(text="✓" if item.is_grid3 else "✗", icon='CHECKMARK' if item.is_grid3 else 'ERROR')


class SKLUM_OT_check_grid3(Operator):
    bl_idname = "sklum.check_grid3"
    bl_label = "Kiểm Tra Số Lưới"
    bl_description = "Kiểm tra các object được chọn có đúng 3 lưới (face) hay không"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(
        name="Chế độ kiểm tra",
        description="Chọn loại mặt để kiểm tra",
        items=[
            ('TRIANGLE', "Tam giác (3 cạnh)", "Kiểm tra các mặt tam giác"),
            ('N-GON', "N-gon (>4 cạnh)", "Kiểm tra các mặt N-gon (nhiều hơn 4 cạnh)"),
        ],
        default='TRIANGLE',
    )

    def execute(self, context):
        scene = context.scene
        scene.sklum_grid3_list.clear()

        found = False
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            mesh = obj.data
            bm = bmesh.from_edit_mesh(mesh)
            bm.faces.ensure_lookup_table()
            for face in bm.faces:
                face.select = False
            for face in bm.faces:
                if self.mode == 'TRIANGLE' and len(face.verts) == 3:
                    face.select = True
                    found = True
                elif self.mode == 'N-GON' and len(face.verts) > 4:
                    face.select = True
                    found = True
            bmesh.update_edit_mesh(mesh, loop_triangles=False, destructive=False)
            bpy.ops.object.mode_set(mode='OBJECT')
            item = scene.sklum_grid3_list.add()
            item.obj_name = obj.name
            item.face_count = len(obj.data.polygons)
            item.is_grid3 = False

        if not context.selected_objects:
            scene.sklum_grid3_check_result = "Chưa chọn vật nào để kiểm tra."
        elif found:
            if self.mode == 'TRIANGLE':
                scene.sklum_grid3_check_result = "Đã chọn các mặt tam giác (triangle) trong edit mode."
            else:
                scene.sklum_grid3_check_result = "Đã chọn các mặt N-gon (>4 cạnh) trong edit mode."
        else:
            if self.mode == 'TRIANGLE':
                scene.sklum_grid3_check_result = "Không tìm thấy mặt tam giác nào."
            else:
                scene.sklum_grid3_check_result = "Không tìm thấy mặt N-gon nào (>4 cạnh)."
        return {'FINISHED'}


classes = (
    SKLUM_MT_grid3_entry,
    SKLUM_UL_grid3_list,
    SKLUM_OT_check_grid3,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sklum_grid3_list = CollectionProperty(type=SKLUM_MT_grid3_entry)
    bpy.types.Scene.sklum_grid3_index = IntProperty()


def unregister():
    del bpy.types.Scene.sklum_grid3_list
    del bpy.types.Scene.sklum_grid3_index
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
