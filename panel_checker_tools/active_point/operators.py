"""Operators for Active Point section"""

import bpy
from math import degrees
from mathutils import Vector
from bpy.types import Operator, PropertyGroup, UIList
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatVectorProperty,
    CollectionProperty,
    IntProperty,
)


class SKLUM_MT_active_point_entry(PropertyGroup):
    obj_name: StringProperty(name="Tên Vật")
    current_origin: FloatVectorProperty(name="Gốc Hiện Tại")
    current_rotation: FloatVectorProperty(name="Rotation Hiện Tại")
    current_scale: FloatVectorProperty(name="Scale Hiện Tại")
    is_standard: BoolProperty(name="Đúng Tiêu Chuẩn")


class SKLUM_UL_active_point_list(UIList):
    bl_idname = "SKLUM_UL_active_point_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.2)
        split.label(text=item.obj_name)

        split = split.split(factor=0.25)
        split.label(text=f"{item.current_origin[0]:.2f}, {item.current_origin[1]:.2f}, {item.current_origin[2]:.2f}")

        split = split.split(factor=0.33)
        split.label(text=f"{item.current_rotation[0]:.1f}, {item.current_rotation[1]:.1f}, {item.current_rotation[2]:.1f}")

        split = split.split(factor=0.5)
        split.label(text=f"{item.current_scale[0]:.2f}, {item.current_scale[1]:.2f}, {item.current_scale[2]:.2f}")

        split.label(text="✓" if item.is_standard else "✗", icon='CHECKMARK' if item.is_standard else 'ERROR')


def calculate_center(obj):
    if obj.type != 'MESH' or len(obj.data.vertices) == 0:
        return obj.location

    bound_box_coords = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    xs = [v.x for v in bound_box_coords]
    ys = [v.y for v in bound_box_coords]
    return Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, 0))


def is_standard_position(current, expected, tolerance=0.001):
    return (
        abs(current.x - expected.x) < tolerance
        and abs(current.y - expected.y) < tolerance
        and abs(current.z) < tolerance
    )


class SKLUM_OT_check_active_point(Operator):
    bl_idname = "sklum.check_active_point"
    bl_label = "Kiểm Tra Active Point"
    bl_description = "Kiểm tra Active Point có nằm ở tâm vật & Z = 0 không"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        sklum = scene.sklum
        scene.sklum_active_point_list.clear()
        sklum.active_point_needs_fix = False

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            expected_origin = calculate_center(obj)
            current_origin = obj.matrix_world.translation.copy()
            rot = obj.rotation_euler.copy()
            scl = obj.scale.copy()

            is_standard = is_standard_position(current_origin, expected_origin)

            item = scene.sklum_active_point_list.add()
            item.obj_name = obj.name
            item.current_origin = current_origin
            item.current_rotation = [degrees(a) for a in rot]
            item.current_scale = scl
            item.is_standard = is_standard

            if not is_standard:
                sklum.active_point_needs_fix = True

        if not context.selected_objects:
            sklum.active_point_check_result = "Chưa chọn vật nào để kiểm tra."
        elif sklum.active_point_needs_fix:
            sklum.active_point_check_result = "Phát hiện lỗi Active Point!"
        else:
            sklum.active_point_check_result = "Tất cả Active Point đều đúng tiêu chuẩn."

        return {'FINISHED'}


class SKLUM_OT_fix_active_point(Operator):
    bl_idname = "sklum.fix_active_point"
    bl_label = "Sửa Active Point"
    bl_description = "Đưa Active Point về tiêu chuẩn: tâm vật & Z = 0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        fixed_count = 0
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)

            center = calculate_center(obj)
            bpy.context.scene.cursor.location = center

            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')
            fixed_count += 1

        self.report({'INFO'}, f"Đã sửa {fixed_count} vật về tiêu chuẩn Active Point.")
        context.scene.sklum.active_point_needs_fix = False
        bpy.ops.sklum.check_active_point('EXEC_DEFAULT')
        return {'FINISHED'}


class SKLUM_OT_group_objects(Operator):
    bl_idname = "sklum.group_objects"
    bl_label = "Gộp về Gốc"
    bl_description = "Tạo Empty và di chuyển các vật đạt tiêu chuẩn về gốc tọa độ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.scene.sklum.active_point_needs_fix:
            self.report({'ERROR'}, "Vui lòng sửa tất cả Active Point trước khi gộp.")
            return {'CANCELLED'}

        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected_meshes:
            self.report({'WARNING'}, "Không có đối tượng MESH nào được chọn.")
            return {'CANCELLED'}

        empty = bpy.data.objects.new("Empty_Group", None)
        context.collection.objects.link(empty)
        empty.location = (0, 0, 0)

        avg_pos = sum((obj.location for obj in selected_meshes), Vector()) / len(selected_meshes)
        context.scene.cursor.location = avg_pos

        for obj in selected_meshes:
            obj.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        for obj in selected_meshes:
            obj.location = (0, 0, 0)

        context.view_layer.objects.active = empty
        for obj in selected_meshes:
            obj.parent = empty
            obj.matrix_parent_inverse = empty.matrix_world.inverted()

        self.report({'INFO'}, "Đã gộp các vật đạt tiêu chuẩn về gốc tọa độ.")
        return {'FINISHED'}


class SKLUM_OT_apply_transforms(Operator):
    bl_idname = "sklum.apply_transforms"
    bl_label = "Apply Rotate & Scale"
    bl_description = "Áp dụng Rotation và Scale mà không thay đổi vị trí"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        self.report({'INFO'}, "Đã áp dụng Rotation và Scale cho các vật được chọn.")
        return {'FINISHED'}


classes = (
    SKLUM_MT_active_point_entry,
    SKLUM_UL_active_point_list,
    SKLUM_OT_check_active_point,
    SKLUM_OT_fix_active_point,
    SKLUM_OT_group_objects,
    SKLUM_OT_apply_transforms,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sklum_active_point_list = CollectionProperty(type=SKLUM_MT_active_point_entry)
    bpy.types.Scene.sklum_active_point_index = IntProperty()


def unregister():
    if hasattr(bpy.types.Scene, 'sklum_active_point_list'):
        del bpy.types.Scene.sklum_active_point_list
    if hasattr(bpy.types.Scene, 'sklum_active_point_index'):
        del bpy.types.Scene.sklum_active_point_index
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
