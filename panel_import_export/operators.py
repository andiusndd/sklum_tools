"""Operators for SKLUM - Import/Export panel"""

import bpy
import os
import sys
import subprocess
from bpy.types import Operator
from bpy.props import StringProperty

from ..core import constants


_pillow_installed = False
try:
    from PIL import Image  # noqa: F401
    _pillow_installed = True
except ImportError:
    pass


def ensure_pillow_is_installed():
    global _pillow_installed
    if _pillow_installed:
        return True, ""

    try:
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--user"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "--user"])

        import site
        user_site_packages = site.getusersitepackages()
        if user_site_packages not in sys.path:
            sys.path.append(user_site_packages)

        from PIL import Image  # noqa: F401
        _pillow_installed = True
        return True, "Pillow was installed successfully."
    except Exception as exc:
        return False, f"Failed to install Pillow: {exc}"


class SKLUM_OT_purge_unused(Operator):
    bl_idname = "sklum.purge_unused"
    bl_label = "Purge Unused Data (Aggressive)"
    bl_description = "Xóa trực tiếp dữ liệu trùng lặp và dọn dẹp dữ liệu không sử dụng"

    def execute(self, context):
        deleted_duplicates = 0

        data_collections = [
            bpy.data.materials,
            bpy.data.images,
            bpy.data.meshes,
            bpy.data.textures,
            bpy.data.actions,
            bpy.data.node_groups,
        ]

        for collection in data_collections:
            deleted_duplicates += self.delete_duplicates(collection)

        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        message = "Dọn dẹp hoàn tất."
        if deleted_duplicates > 0:
            message += f" Đã xóa trực tiếp {deleted_duplicates} dữ liệu trùng lặp."
        self.report({'INFO'}, message)
        return {'FINISHED'}

    def get_base_name_and_suffix(self, name):
        if '.' in name:
            parts = name.split('.')
            if len(parts) > 1 and parts[-1].isdigit():
                suffix = '.' + parts[-1]
                base_name = '.'.join(parts[:-1])
                return base_name, suffix
        return name, None

    def delete_duplicates(self, data_collection):
        count = 0
        items_to_delete = []

        for item in data_collection:
            base_name, suffix = self.get_base_name_and_suffix(item.name)
            if suffix and base_name in data_collection and data_collection[base_name] != item:
                items_to_delete.append(item)

        for item in items_to_delete:
            try:
                is_unloaded_image = False
                if getattr(item, 'source', None) == 'FILE' and getattr(item, 'filepath', ''):
                    abs_path = bpy.path.abspath(item.filepath)
                    if not os.path.exists(abs_path):
                        is_unloaded_image = True
                elif getattr(item, 'source', None) == 'PACKED' and hasattr(item, 'pixels') and not item.pixels:
                    is_unloaded_image = True

                if getattr(item, 'users', 0) == 0 or is_unloaded_image:
                    if item.name in data_collection:
                        data_collection.remove(item)
                        count += 1
            except Exception as exc:
                print(f"Could not delete duplicate '{item.name}': {exc}")

        return count


class SKLUM_OT_pack_textures(Operator):
    bl_idname = "sklum.pack_textures"
    bl_label = "Pack All Textures (JPG Preferred)"
    bl_description = "Chuyển PNG sang JPG nếu có và pack toàn bộ resource"

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report({'ERROR'}, "Vui lòng lưu file Blender trước.")
            return {'CANCELLED'}

        switched_count = 0
        images_to_check = [img for img in bpy.data.images if img.source == 'FILE' and img.filepath]

        for img in images_to_check:
            abs_path = bpy.path.abspath(img.filepath)
            if not os.path.exists(abs_path):
                continue
            base, ext = os.path.splitext(abs_path)
            if ext.lower() == '.png':
                jpg_path = base + '.jpg'
                if os.path.exists(jpg_path):
                    img.filepath = bpy.path.relpath(jpg_path)
                    img.reload()
                    switched_count += 1

        if switched_count > 0:
            self.report({'INFO'}, f"Đã chuyển {switched_count} texture sang .jpg.")

        bpy.ops.file.pack_all()
        self.report({'INFO'}, "Đã pack toàn bộ resource vào file Blender.")
        return {'FINISHED'}


class SKLUM_OT_export_glb(Operator):
    bl_idname = "sklum.export_glb"
    bl_label = "Xuất .GLB"
    bl_description = "Xuất GLB với tên dựa trên IDP"

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report({'ERROR'}, "Bạn cần lưu file Blender trước khi xuất GLB!")
            return {'CANCELLED'}

        settings = context.scene.sklum_auto_rename_settings
        idp = settings.idp.strip()

        if not idp:
            self.report({'ERROR'}, "Trường IDP không được để trống để đặt tên file GLB!")
            return {'CANCELLED'}

        folder = os.path.dirname(bpy.data.filepath)
        filename = f"{idp}.glb"
        filepath = os.path.normpath(bpy.path.abspath(os.path.join(folder, filename)))

        try:
            # Native Blender: If use_selection is True but nothing selected, it might export nothing.
            if not context.selected_objects and constants.EXPORT_GLB_SETTINGS.get('use_selection', True):
                self.report({'WARNING'}, "Chưa chọn đối tượng nào! File GLB có thể không được tạo hoặc bị trống.")

            bpy.ops.export_scene.gltf(
                filepath=filepath,
                **constants.EXPORT_GLB_SETTINGS,
            )
            
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                if size > 0:
                    self.report({'INFO'}, f"Đã xuất GLB thành công ({size/1024:.1f} KB): {filepath}")
                else:
                    self.report({'WARNING'}, f"File GLB đã được tạo nhưng có kích thước 0 bytes: {filepath}")
            else:
                self.report({'ERROR'}, f"Lỗi: Không tìm thấy file GLB sau khi xuất tại {filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Lỗi khi thực thi export_scene.gltf: {str(e)}")
            
        return {'FINISHED'}


class SKLUM_OT_open_native_glb_export(Operator):
    bl_idname = "sklum.open_native_glb_export"
    bl_label = "Mở Export .GLB (Native)"
    bl_description = "Mở hộp thoại Export glTF của Blender"

    def invoke(self, context, event):
        return bpy.ops.export_scene.gltf('INVOKE_DEFAULT', **constants.EXPORT_GLB_SETTINGS)

    def execute(self, context):
        bpy.ops.export_scene.gltf('EXEC_DEFAULT', **constants.EXPORT_GLB_SETTINGS)
        return {'FINISHED'}


class SKLUM_OT_export_fbx(Operator):
    bl_idname = "sklum.export_fbx"
    bl_label = "Xuất .FBX"
    bl_description = "Xuất FBX với tên dựa trên IDP"

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report({'ERROR'}, "Bạn cần lưu file Blender trước khi xuất FBX!")
            return {'CANCELLED'}

        settings = context.scene.sklum_auto_rename_settings
        idp = settings.idp.strip()

        if not idp:
            self.report({'ERROR'}, "Trường IDP không được để trống để đặt tên file FBX!")
            return {'CANCELLED'}

        folder = os.path.dirname(bpy.data.filepath)
        filename = f"{idp}.fbx"
        filepath = os.path.normpath(bpy.path.abspath(os.path.join(folder, filename)))

        try:
            # Native Blender: If use_selection is True but nothing selected, it might export nothing.
            if not context.selected_objects and constants.EXPORT_FBX_SETTINGS.get('use_selection', True):
                self.report({'WARNING'}, "Chưa chọn đối tượng nào! File FBX có thể không được tạo hoặc bị trống.")

            bpy.ops.export_scene.fbx(
                filepath=filepath,
                **constants.EXPORT_FBX_SETTINGS,
            )
            
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                if size > 0:
                    self.report({'INFO'}, f"Đã xuất FBX thành công ({size/1024:.1f} KB): {filepath}")
                else:
                    self.report({'WARNING'}, f"File FBX đã được tạo nhưng có kích thước 0 bytes: {filepath}")
            else:
                self.report({'ERROR'}, f"Lỗi: Không tìm thấy file FBX sau khi xuất tại {filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Lỗi khi thực thi export_scene.fbx: {str(e)}")
            
        return {'FINISHED'}


class SKLUM_OT_import_material_glb(Operator):
    bl_idname = "sklum.import_material_glb"
    bl_label = "Nhập vật liệu (.glb)"
    bl_description = "Nhập vật liệu từ file .glb xuất từ Substance Painter"

    filepath: StringProperty(subtype="FILE_PATH")
    filter_glob: StringProperty(default="*.glb", options={'HIDDEN'})

    def execute(self, context):
        if not self.filepath or not self.filepath.lower().endswith('.glb'):
            self.report({'ERROR'}, "Vui lòng chọn file .glb hợp lệ!")
            return {'CANCELLED'}

        objects_before = set(bpy.data.objects)
        materials_before = set(bpy.data.materials)

        bpy.ops.import_scene.gltf(filepath=self.filepath)

        new_objects = set(bpy.data.objects) - objects_before
        new_materials = set(bpy.data.materials) - materials_before

        if new_objects:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in new_objects:
                obj.select_set(True)
            bpy.ops.object.delete()

        self.report({'INFO'}, f"Đã nhập {len(new_materials)} vật liệu và xóa {len(new_objects)} đối tượng mới.")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class SKLUM_OT_unpack_all_textures(Operator):
    bl_idname = "sklum.unpack_all_textures"
    bl_label = "Unpack & Rename Textures"
    bl_description = "Unpack và đổi tên texture theo quy tắc"

    def execute(self, context):
        settings = context.scene.sklum_auto_rename_settings

        suffix_needed = len(settings.items) > 1
        mat_to_suffix = {}
        if suffix_needed:
            for idx, item in enumerate(settings.items):
                if item.material_name:
                    mat_to_suffix[item.material_name] = f"_{idx+1:02d}"

        bpy.ops.file.unpack_all(method='USE_LOCAL')

        base_name = settings.model_id.strip() if settings.model_id else "texture"
        renamed_count = 0

        for material in bpy.data.materials:
            if not material.use_nodes:
                continue

            suffix = mat_to_suffix.get(material.name, "")

            for node in material.node_tree.nodes:
                if node.type != 'TEX_IMAGE' or not node.image:
                    continue

                tex_suffix = None
                color_space = None

                is_normal = False
                for output in node.outputs:
                    if output.is_linked:
                        for link in output.links:
                            if link.to_node.type == 'NORMAL_MAP':
                                tex_suffix, color_space, _ = constants.NORMAL_MAP_CONFIG
                                is_normal = True
                                break
                        if is_normal:
                            break

                if not is_normal:
                    for output in node.outputs:
                        if output.is_linked:
                            for link in output.links:
                                socket_name = link.to_socket.name
                                if socket_name in constants.TEXTURE_TYPE_MAPPING:
                                    tex_suffix, color_space, _ = constants.TEXTURE_TYPE_MAPPING[socket_name]
                                    break
                        if tex_suffix:
                            break

                if not tex_suffix:
                    search_terms = node.name.lower() + (node.label.lower() if node.label else "")
                    if any(keyword in search_terms for keyword in constants.NORMAL_MAP_CONFIG[2]):
                        tex_suffix, color_space, _ = constants.NORMAL_MAP_CONFIG
                    else:
                        for config in constants.TEXTURE_TYPE_MAPPING.values():
                            if any(keyword in search_terms for keyword in config[2]):
                                tex_suffix, color_space, _ = config
                                break

                if tex_suffix and color_space:
                    new_name = f"{base_name}{tex_suffix}{suffix}"
                    if node.image.name != new_name:
                        node.image.name = new_name
                        renamed_count += 1

                    node.image.colorspace_settings.name = color_space

                    if node.image.source == 'FILE' and node.image.filepath:
                        try:
                            old_filepath = bpy.path.abspath(node.image.filepath)
                            if os.path.exists(old_filepath):
                                file_ext = os.path.splitext(old_filepath)[1]
                                new_filepath = os.path.join(os.path.dirname(old_filepath), f"{new_name}{file_ext}")
                                if old_filepath.lower() != new_filepath.lower():
                                    os.rename(old_filepath, new_filepath)
                                    node.image.filepath = bpy.path.relpath(new_filepath)
                        except Exception as exc:
                            print(f"Lỗi khi đổi tên file texture {old_filepath}: {exc}")

        message = "Đã unpack toàn bộ resource."
        if renamed_count > 0:
            message += f" Đã đổi tên {renamed_count} texture theo quy tắc."
        self.report({'INFO'}, message)
        return {'FINISHED'}


class SKLUM_OT_open_gltf_compressor(Operator):
    """Mở Khronos glTF Compressor trong trình duyệt"""

    bl_idname = "sklum.open_gltf_compressor"
    bl_label = "Open glTF Compressor"
    bl_description = "Mở Khronos glTF Compressor để nén GLB với Draco/KTX2"

    def execute(self, context):
        import webbrowser
        webbrowser.open("https://github.khronos.org/glTF-Compressor-Release/")
        self.report({'INFO'}, "Đã mở Khronos glTF Compressor trong trình duyệt.")
        return {'FINISHED'}


class SKLUM_OT_create_box(Operator):
    bl_idname = "sklum.create_box"
    bl_label = "Tạo Box"
    bl_description = "Tạo Box với kích thước chỉ định, tâm ở đáy, vị trí 0,0,0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.sklum_box_settings
        x, y, z = settings.box_x, settings.box_y, settings.box_z
        
        # Create Cube
        # Create at arbitrary location first to avoid conflict, then move
        bpy.ops.mesh.primitive_cube_add(size=1, align='WORLD', location=(0, 0, 0))
        obj = context.active_object
        
        # Set Dimensions
        obj.dimensions = (x, y, z)
        
        # Apply Scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Set Origin to Bottom
        # 1. Reset origin to geometry center first to be predictable
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
        # 2. Use Cursor to set origin to bottom center
        saved_location = context.scene.cursor.location.copy()
        
        # Since box is centered at (0,0,0) locally relative to its geometry, 
        # and we just set origin to median, the bottom face center is at -z/2 locally.
        # But wait, we need to be careful with world coordinates vs local.
        # The safest way is to use bounding box.
        
        # Get bounds in world space (since we just applied scale)
        import mathutils
        bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
        
        min_z = min(c.z for c in bbox_corners)
        center_x = sum(c.x for c in bbox_corners) / 8
        center_y = sum(c.y for c in bbox_corners) / 8
        
        # Move cursor to bottom center
        context.scene.cursor.location = (center_x, center_y, min_z)
        
        # Set origin to cursor
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Move Object to Global (0,0,0)
        obj.location = (0, 0, 0)
        
        # Restore Cursor
        context.scene.cursor.location = saved_location
        
        self.report({'INFO'}, f"Đã tạo Box {x:.1f}x{y:.1f}x{z:.1f} tại gốc tọa độ.")
        return {'FINISHED'}


classes = (
    SKLUM_OT_purge_unused,
    SKLUM_OT_pack_textures,
    SKLUM_OT_export_glb,
    SKLUM_OT_open_native_glb_export,
    SKLUM_OT_export_fbx,
    SKLUM_OT_import_material_glb,
    SKLUM_OT_unpack_all_textures,
    SKLUM_OT_open_gltf_compressor,
    SKLUM_OT_create_box,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
