"""Operators for Color Space section"""

import bpy
from bpy.types import Operator, PropertyGroup, UIList
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    PointerProperty,
    CollectionProperty,
)

from ...core import constants


class SKLUM_PG_color_space_entry(PropertyGroup):
    node_name: StringProperty(name="Tên Node")
    node_label: StringProperty(name="Node Label")
    current_space: StringProperty(name="Color Space Hiện Tại")
    is_base_color: BoolProperty(name="Là Base Color")
    image_name: StringProperty(name="Tên Ảnh", default="")
    mat_name: StringProperty(name="Tên Material", default="")
    image: PointerProperty(type=bpy.types.Image)


class SKLUM_UL_color_space_list(UIList):
    bl_idname = "SKLUM_UL_color_space_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.2)
        split.label(text=item.node_label or item.node_name, translate=False)

        split = split.split(factor=0.4)
        split.label(text=item.mat_name, translate=False)

        split = split.split(factor=0.5)
        split.label(text=item.current_space, translate=False)

        split = split.split(factor=0.5)
        split.label(text=item.image_name or "<None>", translate=False)

        op = split.operator("sklum.replace_jpg_image", text=".JPG", icon='FILEBROWSER', emboss=True)
        op.item_index = index


def get_expected_color_space(node):
    for output in node.outputs:
        if output.is_linked:
            for link in output.links:
                if link.to_node.type == 'NORMAL_MAP':
                    return constants.NORMAL_MAP_CONFIG[1]
                if link.to_node.type == 'BSDF_PRINCIPLED' and link.to_socket.name == 'Alpha':
                    return constants.COLOR_SPACE_NON_COLOR

    for output in node.outputs:
        if output.is_linked:
            for link in output.links:
                socket_name = link.to_socket.name
                if socket_name in constants.TEXTURE_TYPE_MAPPING:
                    return constants.TEXTURE_TYPE_MAPPING[socket_name][1]

    return constants.COLOR_SPACE_NON_COLOR


class SKLUM_OT_check_color_space(Operator):
    bl_idname = "sklum.check_color_space"
    bl_label = "Kiểm Tra Color Space"
    bl_description = "Kiểm tra Color Space của các node Image Texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        sklum = scene.sklum
        scene.sklum_color_space_list.clear()
        sklum.color_space_needs_fix = False

        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue
            for node in mat.node_tree.nodes:
                if node.type != 'TEX_IMAGE' or not node.image:
                    continue

                expected_space = get_expected_color_space(node)

                item = scene.sklum_color_space_list.add()
                item.node_name = node.name
                item.node_label = node.label if node.label else ""
                item.current_space = node.image.colorspace_settings.name
                item.is_base_color = (expected_space == constants.COLOR_SPACE_SRGB)
                item.image = node.image
                item.image_name = node.image.name
                item.mat_name = mat.name

                if node.image.colorspace_settings.name != expected_space:
                    sklum.color_space_needs_fix = True

        if not any(mat.use_nodes for mat in bpy.data.materials):
            sklum.color_space_check_result = "Không có material nào để kiểm tra."
        elif sklum.color_space_needs_fix:
            sklum.color_space_check_result = "Phát hiện lỗi Color Space!"
        else:
            sklum.color_space_check_result = "Tất cả Color Space đều đúng tiêu chuẩn."

        return {'FINISHED'}


class SKLUM_OT_fix_color_space(Operator):
    bl_idname = "sklum.fix_color_space"
    bl_label = "Sửa Color Space"
    bl_description = "Áp dụng tiêu chuẩn Color Space"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        fixed_count = 0
        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue
            for node in mat.node_tree.nodes:
                if node.type != 'TEX_IMAGE' or not node.image:
                    continue

                expected_space = get_expected_color_space(node)
                if node.image.colorspace_settings.name != expected_space:
                    node.image.colorspace_settings.name = expected_space
                    fixed_count += 1

        self.report({'INFO'}, f"Đã sửa {fixed_count} node không đúng tiêu chuẩn.")
        context.scene.sklum.color_space_needs_fix = False
        bpy.ops.sklum.check_color_space('EXEC_DEFAULT')
        return {'FINISHED'}


class SKLUM_OT_replace_jpg_image(Operator):
    bl_idname = "sklum.replace_jpg_image"
    bl_label = "Thay .JPG"
    bl_description = "Chọn file JPG để thay thế ảnh cho node Image Texture"

    filepath: StringProperty(subtype="FILE_PATH", options={'HIDDEN'})
    filter_glob: StringProperty(default="*.jpg;*.jpeg", options={'HIDDEN'})
    item_index: IntProperty()

    def execute(self, context):
        scene = context.scene
        item = scene.sklum_color_space_list[self.item_index]
        mat = bpy.data.materials.get(item.mat_name)
        if not mat or not mat.use_nodes:
            self.report({'ERROR'}, "Không tìm thấy material hoặc material không dùng node!")
            return {'CANCELLED'}
        node = mat.node_tree.nodes.get(item.node_name)
        if not node or node.type != 'TEX_IMAGE':
            self.report({'ERROR'}, "Không tìm thấy node Image Texture!")
            return {'CANCELLED'}

        try:
            img = bpy.data.images.load(self.filepath, check_existing=True)
        except Exception as exc:
            self.report({'ERROR'}, f"Không thể load ảnh: {exc}")
            return {'CANCELLED'}

        node.image = img
        item.image = img
        item.image_name = img.name
        self.report({'INFO'}, f"Đã thay ảnh JPG cho node {node.name}")

        bpy.ops.sklum.check_color_space('EXEC_DEFAULT')
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


classes = (
    SKLUM_PG_color_space_entry,
    SKLUM_UL_color_space_list,
    SKLUM_OT_check_color_space,
    SKLUM_OT_fix_color_space,
    SKLUM_OT_replace_jpg_image,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sklum_color_space_list = CollectionProperty(type=SKLUM_PG_color_space_entry)
    bpy.types.Scene.sklum_color_space_index = IntProperty()


def unregister():
    if hasattr(bpy.types.Scene, 'sklum_color_space_list'):
        del bpy.types.Scene.sklum_color_space_list
    if hasattr(bpy.types.Scene, 'sklum_color_space_index'):
        del bpy.types.Scene.sklum_color_space_index
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
