"""Operators cho tính năng Auto Rename"""

import os

import bpy
from bpy.types import Operator
from bpy.props import StringProperty

from ..core import constants
from . import utils


class SKLUM_OT_SetPresetValue(Operator):
    """Đặt giá trị preset vào thuộc tính đích"""

    bl_idname = "sklum.set_preset_value"
    bl_label = "Set Preset Value"

    value: StringProperty()
    target_prop: StringProperty()
    target_context: StringProperty(default="sklum_auto_rename_settings")

    def execute(self, context):
        settings = getattr(context.scene, self.target_context, None)
        if not settings:
            self.report({'ERROR'}, f"Không tìm thấy context '{self.target_context}'.")
            return {'CANCELLED'}

        if self.target_prop in {"model_type", "main_material"}:
            target = settings
        else:
            if not settings.items or settings.active_index >= len(settings.items):
                self.report({'WARNING'}, "Không có mục nào đang được chọn trong danh sách.")
                return {'CANCELLED'}
            target = settings.items[settings.active_index]

        setattr(target, self.target_prop, self.value)
        return {'FINISHED'}


class SKLUM_OT_AddPreset(Operator):
    bl_idname = "sklum.add_preset"
    bl_label = "Add Preset"
    bl_description = "Thêm giá trị hiện tại vào danh sách preset"

    preset_type: StringProperty()
    value_to_add: StringProperty()

    def execute(self, context):
        utils.add_preset(self.preset_type, self.value_to_add)
        self.report({'INFO'}, f"Đã thêm preset '{self.value_to_add}' vào '{self.preset_type}'.")
        return {'FINISHED'}


class SKLUM_OT_AutoRenameAddItem(Operator):
    bl_idname = "sklum.auto_rename_add_item"
    bl_label = "Thêm"
    bl_description = "Thêm các đối tượng mesh đang chọn vào danh sách đổi tên"

    @classmethod
    def poll(cls, context):
        return context.selected_objects and any(obj.type == 'MESH' for obj in context.selected_objects)

    def execute(self, context):
        settings = context.scene.sklum_auto_rename_settings
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']

        for obj in selected_meshes:
            if any(item.original_name == obj.name for item in settings.items):
                continue
            new_item = settings.items.add()
            new_item.original_name = obj.name
            new_item.mesh_name = obj.name
            if obj.active_material:
                new_item.material_name = obj.active_material.name

        settings.active_index = max(0, len(settings.items) - 1)
        return {'FINISHED'}


class SKLUM_OT_AutoRenameRemoveItem(Operator):
    bl_idname = "sklum.auto_rename_remove_item"
    bl_label = "Xóa"
    bl_description = "Xóa mục đã chọn khỏi danh sách"

    @classmethod
    def poll(cls, context):
        settings = context.scene.sklum_auto_rename_settings
        return settings.items and settings.active_index < len(settings.items)

    def execute(self, context):
        settings = context.scene.sklum_auto_rename_settings
        settings.items.remove(settings.active_index)
        if settings.active_index >= len(settings.items):
            settings.active_index = max(0, len(settings.items) - 1)
        return {'FINISHED'}


class SKLUM_OT_AutoRenameClearList(Operator):
    bl_idname = "sklum.auto_rename_clear_list"
    bl_label = "Xóa Tất Cả"
    bl_description = "Xóa toàn bộ danh sách đổi tên"

    @classmethod
    def poll(cls, context):
        return bool(context.scene.sklum_auto_rename_settings.items)

    def execute(self, context):
        context.scene.sklum_auto_rename_settings.items.clear()
        return {'FINISHED'}


class SKLUM_OT_LoadIDPCsv(Operator):
    bl_idname = "sklum.load_idp_csv"
    bl_label = "Nhập"
    bl_description = "Tải hoặc tải lại dữ liệu IDP/Collection từ file CSV"

    def execute(self, context):
        settings = context.scene.sklum_auto_rename_settings
        filepath = settings.csv_filepath

        if not filepath or not os.path.exists(filepath):
            self.report({'ERROR'}, "Đường dẫn file CSV không hợp lệ hoặc file không tồn tại.")
            return {'CANCELLED'}

        success, message = utils.load_idp_data_from_csv(filepath)
        if success:
            utils.set_last_loaded_csv(filepath)
            self.report({'INFO'}, message)
        else:
            utils.set_last_loaded_csv(None)
            self.report({'ERROR'}, message)
        return {'FINISHED'}


class SKLUM_OT_AutoRenameExecute(Operator):
    bl_idname = "sklum.auto_rename_execute"
    bl_label = "Đổi"

    def execute(self, context):
        settings = context.scene.sklum_auto_rename_settings
        if not settings.items:
            self.report({'WARNING'}, "Danh sách đổi tên đang trống.")
            return {'CANCELLED'}

        utils.add_preset("model_types", settings.model_type)
        for item in settings.items:
            utils.add_preset("mesh_names", item.mesh_name)
            utils.add_preset("material_names", item.material_name)

        parent_empty = next((obj for obj in context.scene.objects if obj.type == 'EMPTY' and obj.parent is None), None)
        if not parent_empty:
            self.report({'ERROR'}, "Không tìm thấy Empty gốc trong scene.")
            return {'CANCELLED'}

        base_parent_name = f"{settings.model_id}_{settings.model_type} {settings.main_material}".strip()
        if base_parent_name:
            parent_empty.name = base_parent_name

        suffix_needed = len(settings.items) > 1

        for index, item in enumerate(settings.items, start=1):
            obj = context.scene.objects.get(item.original_name) or context.scene.objects.get(item.mesh_name)
            if not obj or obj.type != 'MESH':
                self.report({'WARNING'}, f"Không tìm thấy mesh '{item.original_name}'.")
                continue

            obj.name = item.mesh_name

            if obj.data:
                base_data_name = settings.idp.strip() if settings.idp.strip() else item.mesh_name
                data_suffix = f"_{index:02d}" if suffix_needed else ""
                obj.data.name = f"{base_data_name}{data_suffix}"

            item.original_name = item.mesh_name

            if obj.data and getattr(obj.data, 'materials', None):
                material = obj.data.materials[0]
                if material:
                    material.name = item.material_name
                    self._rename_textures(material, settings, index, suffix_needed)

        self.report({'INFO'}, "Hoàn tất đổi tên.")
        return {'FINISHED'}

    def _rename_textures(self, material, settings, index, suffix_needed):
        if not material.use_nodes:
            return

        suffix = f"_{index:02d}" if suffix_needed else ""
        base_name = settings.model_id

        for node in material.node_tree.nodes:
            if node.type != 'TEX_IMAGE' or not node.image:
                continue

            tex_suffix = None
            color_space = None
            node_label_name = None

            # 1. Trace Connections (Universal Priority - Supports Multiple Sockets)
            # Returns a set of socket names, e.g. {"Metallic", "Roughness"}
            bsdf_sockets = self._trace_to_principled_bsdf(node)
            
            if bsdf_sockets:
                # Node Label: Join all socket names with spaces and uppercase
                # e.g. "METALLIC ROUGHNESS"
                # Use sorted list for consistent label order
                sorted_sockets = sorted(list(bsdf_sockets))
                node_label_name = " ".join(sorted_sockets)
                
                # File Suffix: Find common suffix for these sockets
                # Priority: If any socket is in mapping, use its suffix. 
                # If multiple different suffixes, pick the first one from sorted list.
                found_suffixes = []
                for s_name in sorted_sockets:
                    if s_name in constants.TEXTURE_TYPE_MAPPING:
                        res = constants.TEXTURE_TYPE_MAPPING[s_name]
                        found_suffixes.append((res[0], res[1])) # (suffix, colorspace)
                
                if found_suffixes:
                    # Pick unique suffixes. Usually they share one (like _RMA) 
                    # If they differ, we pick the first one encountered in sorted socket list.
                    tex_suffix, color_space = found_suffixes[0]
                else:
                    # Fallback: use first socket name directly if not in mapping
                    first_socket = sorted_sockets[0]
                    tex_suffix = f"_{first_socket.replace(' ', '')}"
                    color_space = constants.COLOR_SPACE_NON_COLOR

            # 2. Fallback to keyword-based detection (Last Priority)
            if not tex_suffix:
                search_terms = node.name.lower() + (node.label.lower() if node.label else "")
                # Check mapping keywords first
                for key, config in constants.TEXTURE_TYPE_MAPPING.items():
                    if any(keyword in search_terms for keyword in config[2]):
                        tex_suffix, color_space, _ = config
                        node_label_name = key
                        break
                
                # Check special normal config if still not found
                if not tex_suffix:
                    if any(keyword in search_terms for keyword in constants.NORMAL_MAP_CONFIG[2]):
                        tex_suffix, color_space, _ = constants.NORMAL_MAP_CONFIG
                        node_label_name = "Normal"

            if tex_suffix and color_space:
                new_name = f"{base_name}{tex_suffix}{suffix}" if base_name else f"Texture{tex_suffix}{suffix}"
                
                # Rename node label (e.g., "METALLIC ROUGHNESS")
                if node_label_name:
                    final_label = node_label_name.upper() # User requested spaces, no underscores
                    if node.label != final_label:
                        node.label = final_label
                
                # Rename image datablock
                if node.image.name != new_name:
                    node.image.name = new_name
                node.image.colorspace_settings.name = color_space

                # Rename file on disk
                if node.image.source == 'FILE' and node.image.filepath:
                    try:
                        old_filepath = bpy.path.abspath(node.image.filepath)
                        if os.path.exists(old_filepath):
                            ext = os.path.splitext(old_filepath)[1]
                            new_filepath = os.path.join(os.path.dirname(old_filepath), f"{new_name}{ext}")
                            if old_filepath.lower() != new_filepath.lower():
                                os.rename(old_filepath, new_filepath)
                                node.image.filepath = bpy.path.relpath(new_filepath)
                    except Exception as exc:
                        print(f"Lỗi khi đổi tên file texture {node.image.name}: {exc}")

    def _trace_to_principled_bsdf(self, start_node, visited=None, depth=0):
        """
        Trace từ một node texture để tìm TẤT CẢ các socket của Principled BSDF mà nó kết nối đến.
        Returns: set() chứa các tên socket (e.g., {"Metallic", "Roughness"})
        """
        if visited is None:
            visited = set()

        sockets_found = set()

        if depth > 10 or start_node in visited:
            return sockets_found

        visited.add(start_node)

        for output in start_node.outputs:
            if not output.is_linked:
                continue

            for link in output.links:
                to_node = link.to_node
                to_socket = link.to_socket

                # Found Principled BSDF connection
                if to_node.type == 'BSDF_PRINCIPLED':
                    sockets_found.add(to_socket.name)
                else:
                    # Continue tracing through intermediate nodes
                    sockets_found.update(self._trace_to_principled_bsdf(to_node, visited, depth + 1))

        return sockets_found


classes = (
    SKLUM_OT_SetPresetValue,
    SKLUM_OT_AddPreset,
    SKLUM_OT_AutoRenameAddItem,
    SKLUM_OT_AutoRenameRemoveItem,
    SKLUM_OT_AutoRenameClearList,
    SKLUM_OT_LoadIDPCsv,
    SKLUM_OT_AutoRenameExecute,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
