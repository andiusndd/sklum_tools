"""Operators for Seam & Sharp section"""

import bpy
import bmesh
from bpy.types import Operator, PropertyGroup, UIList
from bpy.props import (
    StringProperty,
    BoolProperty,
    CollectionProperty,
    IntProperty,
)


class SKLUM_MT_seam_entry(PropertyGroup):
    obj_name: StringProperty(name="Tên Vật")
    has_seam: BoolProperty(name="Có Seam")


class SKLUM_UL_seam_list(UIList):
    bl_idname = "SKLUM_UL_seam_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.7)
        split.label(text=item.obj_name)
        split.label(text="✓" if item.has_seam else "✗", icon='CHECKMARK' if item.has_seam else 'ERROR')


class SKLUM_OT_check_seam(Operator):
    bl_idname = "sklum.check_seam"
    bl_label = "Kiểm Tra Seam"
    bl_description = "Kiểm tra xem vật có đánh dấu Seam chưa"
    bl_options = {'REGISTER', 'UNDO'}

    def _check_object_seams(self, obj):
        if obj.type != 'MESH' or not obj.data.edges:
            return False
        return any(edge.use_seam for edge in obj.data.edges)

    def execute(self, context):
        scene = context.scene
        scene.sklum_seam_list.clear()
        scene.sklum_seam_needs_mark = False

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            has_seam = self._check_object_seams(obj)
            item = scene.sklum_seam_list.add()
            item.obj_name = obj.name
            item.has_seam = has_seam

            if not has_seam:
                scene.sklum_seam_needs_mark = True

        if not context.selected_objects:
            scene.sklum_seam_check_result = "Chưa chọn vật nào để kiểm tra."
        elif scene.sklum_seam_needs_mark:
            scene.sklum_seam_check_result = "Phát hiện vật chưa có Seam!"
        else:
            scene.sklum_seam_check_result = "Tất cả vật được chọn đều đã có Seam."

        return {'FINISHED'}


class SKLUM_OT_mark_seam_from_uv(Operator):
    bl_idname = "sklum.mark_seam_from_uv"
    bl_label = "Mark Seam From UV Islands"
    bl_description = "Đánh dấu Seam từ viền ngoài của UV islands"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        area_to_use = None
        max_size = 0
        for area in context.screen.areas:
            if area.type in {'VIEW_3D', 'CONSOLE'}:
                size = area.width * area.height
                if size > max_size:
                    max_size = size
                    area_to_use = area

        if not area_to_use:
            self.report({'ERROR'}, "Không tìm thấy không gian phù hợp để chạy tác vụ UV.")
            return {'CANCELLED'}

        original_type = area_to_use.type
        area_to_use.type = 'IMAGE_EDITOR'
        area_to_use.ui_type = 'UV'

        tool_settings = context.tool_settings
        original_sync_state = tool_settings.use_uv_sync_selection
        tool_settings.use_uv_sync_selection = True

        fixed_count = 0
        try:
            for obj in context.selected_objects:
                if obj.type != 'MESH':
                    continue

                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.uv.seams_from_islands()
                bpy.ops.object.mode_set(mode='OBJECT')
                fixed_count += 1
        finally:
            tool_settings.use_uv_sync_selection = original_sync_state
            area_to_use.type = original_type

        if fixed_count > 0:
            self.report({'INFO'}, f"Đã đánh dấu Seam từ UV cho {fixed_count} vật.")
        else:
            self.report({'WARNING'}, "Không có vật nào được xử lý.")

        context.scene.sklum_seam_needs_mark = False
        bpy.ops.sklum.check_seam('EXEC_DEFAULT')
        return {'FINISHED'}


class SKLUM_OT_clear_sharp_edges(Operator):
    bl_idname = "sklum.clear_sharp_edges"
    bl_label = "Clear Sharp"
    bl_description = "Loại bỏ thuộc tính Sharp, chuyển tất cả cạnh về Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = 0
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                mesh = obj.data
                bm = bmesh.new()
                bm.from_mesh(mesh)
                for edge in bm.edges:
                    edge.smooth = True
                bm.to_mesh(mesh)
                bm.free()
                mesh.update()
                count += 1
        self.report({'INFO'}, f"Đã loại bỏ Sharp cho {count} vật.")
        return {'FINISHED'}


class SKLUM_OT_clear_seam(Operator):
    bl_idname = "sklum.clear_seam"
    bl_label = "Clear Seam"
    bl_description = "Xóa tất cả Seam trên các mesh được chọn"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = 0
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                mesh = obj.data
                bm = bmesh.new()
                bm.from_mesh(mesh)
                for edge in bm.edges:
                    edge.seam = False
                bm.to_mesh(mesh)
                bm.free()
                mesh.update()
                count += 1
        self.report({'INFO'}, f"Đã xóa Seam cho {count} mesh được chọn.")
        return {'FINISHED'}


class SKLUM_OT_convert_sharp_to_seam(Operator):
    bl_idname = "sklum.convert_sharp_to_seam"
    bl_label = "Convert Sharp to Seam"
    bl_description = "Chuyển các cạnh Sharp thành Mark Seam và sau đó Clear Sharp"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        converted_count = 0
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            mesh = obj.data
            bm = bmesh.new()
            bm.from_mesh(mesh)

            edges_to_change = [edge for edge in bm.edges if not edge.smooth]
            if edges_to_change:
                for edge in edges_to_change:
                    edge.seam = True
                    edge.smooth = True

                bm.to_mesh(mesh)
                converted_count += 1

            bm.free()
            mesh.update()

        if converted_count > 0:
            self.report({'INFO'}, f"Đã chuyển cạnh Sharp thành Seam cho {converted_count} vật.")
        else:
            self.report({'INFO'}, "Không tìm thấy cạnh Sharp nào để chuyển đổi.")

        bpy.ops.sklum.check_seam('EXEC_DEFAULT')
        return {'FINISHED'}


classes = (
    SKLUM_MT_seam_entry,
    SKLUM_UL_seam_list,
    SKLUM_OT_check_seam,
    SKLUM_OT_mark_seam_from_uv,
    SKLUM_OT_clear_sharp_edges,
    SKLUM_OT_clear_seam,
    SKLUM_OT_convert_sharp_to_seam,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sklum_seam_list = CollectionProperty(type=SKLUM_MT_seam_entry)
    bpy.types.Scene.sklum_seam_index = IntProperty()


def unregister():
    del bpy.types.Scene.sklum_seam_list
    del bpy.types.Scene.sklum_seam_index
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
