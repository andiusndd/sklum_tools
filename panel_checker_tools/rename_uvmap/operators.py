"""Operators & property groups for Rename & UVMap section"""

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty


class SKLUM_MT_rename_entry(PropertyGroup):
    obj_type: StringProperty(name="Loại")
    obj_name: StringProperty(name="Tên")
    mat_name: StringProperty(name="Tên Material", default="")
    is_renaming: BoolProperty(default=False)
    new_name: StringProperty(name="Tên mới", default="")


class SKLUM_OT_rename_start(Operator):
    bl_idname = "sklum.rename_start"
    bl_label = "Start Renaming"
    index: IntProperty()

    def execute(self, context):
        items = context.scene.sklum_rename_list
        for i, item in enumerate(items):
            item.is_renaming = (i == self.index)
            if i == self.index:
                item.new_name = item.obj_name
        return {'FINISHED'}


class SKLUM_OT_rename_confirm(Operator):
    bl_idname = "sklum.rename_confirm"
    bl_label = "Confirm Rename"
    index: IntProperty()

    def execute(self, context):
        items = context.scene.sklum_rename_list
        item = items[self.index]
        new_name = item.new_name.strip()
        if not new_name:
            self.report({'ERROR'}, "New name cannot be empty!")
            return {'CANCELLED'}

        try:
            if item.obj_type == 'OBJECT':
                bpy.data.objects[item.obj_name].name = new_name
            elif item.obj_type == 'EMPTY':
                bpy.data.objects[item.obj_name].name = new_name
            elif item.obj_type == 'MATERIAL':
                bpy.data.materials[item.mat_name].name = new_name
            elif item.obj_type == 'IMAGE':
                bpy.data.images[item.obj_name].name = new_name
        except (KeyError, ReferenceError) as exc:
            self.report({'ERROR'}, f"Could not find item to rename: {exc}")
            return {'CANCELLED'}

        item.is_renaming = False
        bpy.ops.sklum.refresh_rename_list('EXEC_DEFAULT')
        return {'FINISHED'}


class SKLUM_OT_refresh_rename_list(Operator):
    bl_idname = "sklum.refresh_rename_list"
    bl_label = "Refresh Rename List"

    def execute(self, context):
        scene = context.scene
        scene.sklum_rename_list.clear()

        for obj in bpy.data.objects:
            if obj.type == 'EMPTY':
                item = scene.sklum_rename_list.add()
                item.obj_type = 'EMPTY'
                item.obj_name = obj.name

        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                item = scene.sklum_rename_list.add()
                item.obj_type = 'OBJECT'
                item.obj_name = obj.name
                if obj.data.materials:
                    item.mat_name = obj.data.materials[0].name

                for mat in obj.data.materials:
                    if mat:
                        mat_item = scene.sklum_rename_list.add()
                        mat_item.obj_type = 'MATERIAL'
                        mat_item.obj_name = obj.name
                        mat_item.mat_name = mat.name

        for mat in bpy.data.materials:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        if not any(
                            i.obj_name == node.image.name and i.obj_type == 'IMAGE'
                            for i in scene.sklum_rename_list
                        ):
                            img_item = scene.sklum_rename_list.add()
                            img_item.obj_type = 'IMAGE'
                            img_item.obj_name = node.image.name
                            img_item.mat_name = mat.name
        return {'FINISHED'}


class SKLUM_OT_reset_uvmap(Operator):
    bl_idname = "sklum.reset_uvmap"
    bl_label = "Reset UVMap"
    bl_description = "Đổi tên UV map đang active thành 'UVMap' cho các object được chọn"

    def execute(self, context):
        count = 0
        for obj in context.selected_objects:
            if obj.type == 'MESH' and obj.data.uv_layers.active:
                uv_layer = obj.data.uv_layers.active
                if uv_layer.name != 'UVMap':
                    uv_layer.name = 'UVMap'
                    count += 1
        self.report({'INFO'}, f"Đã đặt lại tên UVMap cho {count} object.")
        return {'FINISHED'}


classes = (
    SKLUM_MT_rename_entry,
    SKLUM_OT_rename_start,
    SKLUM_OT_rename_confirm,
    SKLUM_OT_refresh_rename_list,
    SKLUM_OT_reset_uvmap,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sklum_rename_list = CollectionProperty(type=SKLUM_MT_rename_entry)
    bpy.types.Scene.sklum_rename_index = IntProperty()


def unregister():
    del bpy.types.Scene.sklum_rename_list
    del bpy.types.Scene.sklum_rename_index
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
