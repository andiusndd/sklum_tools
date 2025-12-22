"""Operators cho panel JPG Converter"""

import bpy
import os
from bpy.types import Operator
from bpy.props import IntProperty, BoolProperty

from .utils import ensure_pillow_is_installed


class SKLUM_OT_OpenConverterPopup(Operator):
    """Mở popup để convert PNG sang JPG với settings chi tiết"""

    bl_idname = "sklum.open_converter_popup"
    bl_label = "PNG to JPG Converter"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        # Scan và populate danh sách PNG textures
        self.refresh_texture_list(context)

        # Mở popup dialog
        return context.window_manager.invoke_props_dialog(self, width=450)

    def refresh_texture_list(self, context):
        """Scan tất cả PNG textures trong file và populate list"""
        settings = context.scene.sklum_converter_settings
        settings.items.clear()

        for img in bpy.data.images:
            if img.source == 'PACKED':
                continue
            if not img.filepath:
                continue

            abs_path = bpy.path.abspath(img.filepath)
            if not abs_path.lower().endswith('.png'):
                continue
            if not os.path.exists(abs_path):
                continue

            item = settings.items.add()
            item.image_name = img.name
            item.filepath = abs_path
            item.enabled = True
            item.use_custom_quality = False
            item.quality = settings.global_quality

    def draw(self, context):
        layout = self.layout
        settings = context.scene.sklum_converter_settings

        # Header với global quality
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Chất lượng chung:", icon='SETTINGS')
        row.prop(settings, "global_quality", text="")

        # Option xóa PNG sau convert
        row = box.row()
        row.prop(settings, "delete_png_after", text="Xóa file PNG sau khi convert")

        layout.separator()

        # Texture list
        if settings.items:
            row = layout.row()
            row.label(text=f"Tìm thấy {len(settings.items)} textures PNG:", icon='IMAGE_DATA')

            # Split layout: list on left, preview on right
            split = layout.split(factor=0.6)

            # Left column: texture list
            col_left = split.column()
            col_left.template_list(
                "SKLUM_UL_ConverterTextureList",
                "",
                settings,
                "items",
                settings,
                "active_index",
                rows=min(6, max(3, len(settings.items))),
            )

            # Right column: preview
            col_right = split.column()
            if settings.items and 0 <= settings.active_index < len(settings.items):
                active_item = settings.items[settings.active_index]
                img = bpy.data.images.get(active_item.image_name)
                if img:
                    # Force generate preview if not exists
                    if img.preview is None or img.preview.icon_id == 0:
                        img.preview_ensure()

                    # Use template_icon for proper preview display
                    preview_box = col_right.box()
                    preview_box.template_icon(icon_value=img.preview.icon_id, scale=8.0)
                    col_right.label(text=active_item.image_name)
                else:
                    col_right.label(text="Image not found", icon='ERROR')
            else:
                col_right.label(text="Chọn texture để xem preview", icon='INFO')

            # Action buttons
            row = layout.row(align=True)
            row.operator("sklum.converter_select_all", text="Chọn tất cả", icon='CHECKBOX_HLT')
            row.operator("sklum.converter_deselect_all", text="Bỏ chọn", icon='CHECKBOX_DEHLT')
            row.operator("sklum.converter_refresh_list", text="", icon='FILE_REFRESH')

            # Count enabled
            enabled_count = sum(1 for item in settings.items if item.enabled)
            layout.label(text=f"Sẽ convert: {enabled_count}/{len(settings.items)} textures")
        else:
            box = layout.box()
            box.label(text="Không tìm thấy texture PNG nào đã unpack.", icon='INFO')
            box.label(text="Hãy unpack textures trước khi convert.")

    def execute(self, context):
        success, message = ensure_pillow_is_installed()
        if not success:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}
        if "installed successfully" in message:
            self.report({'INFO'}, message)

        from PIL import Image

        if not bpy.data.is_saved:
            self.report({'ERROR'}, "Vui lòng lưu file Blender trước.")
            return {'CANCELLED'}

        settings = context.scene.sklum_converter_settings
        count = 0
        errors = 0

        for item in settings.items:
            if not item.enabled:
                continue

            try:
                abs_path = item.filepath
                if not os.path.exists(abs_path):
                    continue

                # Determine quality
                quality = item.quality if item.use_custom_quality else settings.global_quality

                # Convert
                jpg_path = os.path.splitext(abs_path)[0] + '.jpg'
                pil_img = Image.open(abs_path).convert('RGB')
                pil_img.save(jpg_path, 'JPEG', quality=quality)

                # Update Blender image reference
                img = bpy.data.images.get(item.image_name)
                if img:
                    img.filepath = bpy.path.relpath(jpg_path)
                    img.reload()

                # Delete PNG if option enabled
                if settings.delete_png_after:
                    try:
                        os.remove(abs_path)
                    except Exception:
                        pass

                count += 1

            except Exception as exc:
                self.report({'WARNING'}, f"Lỗi chuyển đổi {item.image_name}: {exc}")
                errors += 1

        message = f"Đã convert {count} textures sang JPG."
        if errors > 0:
            message += f" {errors} lỗi."
        self.report({'INFO'}, message)
        return {'FINISHED'}


class SKLUM_OT_ConverterSelectAll(Operator):
    """Chọn tất cả textures trong danh sách"""

    bl_idname = "sklum.converter_select_all"
    bl_label = "Chọn tất cả"

    def execute(self, context):
        settings = context.scene.sklum_converter_settings
        for item in settings.items:
            item.enabled = True
        return {'FINISHED'}


class SKLUM_OT_ConverterDeselectAll(Operator):
    """Bỏ chọn tất cả textures"""

    bl_idname = "sklum.converter_deselect_all"
    bl_label = "Bỏ chọn tất cả"

    def execute(self, context):
        settings = context.scene.sklum_converter_settings
        for item in settings.items:
            item.enabled = False
        return {'FINISHED'}


class SKLUM_OT_ConverterRefreshList(Operator):
    """Refresh danh sách textures PNG"""

    bl_idname = "sklum.converter_refresh_list"
    bl_label = "Refresh"

    def execute(self, context):
        settings = context.scene.sklum_converter_settings
        settings.items.clear()

        for img in bpy.data.images:
            if img.source == 'PACKED':
                continue
            if not img.filepath:
                continue

            abs_path = bpy.path.abspath(img.filepath)
            if not abs_path.lower().endswith('.png'):
                continue
            if not os.path.exists(abs_path):
                continue

            item = settings.items.add()
            item.image_name = img.name
            item.filepath = abs_path
            item.enabled = True
            item.use_custom_quality = False
            item.quality = settings.global_quality

        self.report({'INFO'}, f"Đã tìm thấy {len(settings.items)} textures PNG.")
        return {'FINISHED'}


# Legacy operators for backward compatibility
class SKLUM_OT_convert_png_to_jpg_quality(Operator):
    """Convert tất cả PNG sang JPG với quality chỉ định (legacy)"""

    bl_idname = "sklum.convert_png_to_jpg_quality"
    bl_label = "Chuyển .PNG Sang .JPG"
    bl_description = "Chuyển đổi các texture PNG đã unpack thành JPG"
    bl_options = {'REGISTER', 'UNDO'}

    quality: IntProperty(name="Chất lượng JPG", default=95, min=1, max=100)

    def execute(self, context):
        success, message = ensure_pillow_is_installed()
        if not success:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}

        from PIL import Image

        if not bpy.data.is_saved:
            self.report({'ERROR'}, "Vui lòng lưu file Blender trước.")
            return {'CANCELLED'}

        count = 0
        for img in list(bpy.data.images):
            if img.source == 'PACKED' or not img.filepath:
                continue

            try:
                abs_path = bpy.path.abspath(img.filepath)
                if not abs_path.lower().endswith('.png'):
                    continue
                if not os.path.exists(abs_path):
                    continue

                jpg_path = os.path.splitext(abs_path)[0] + '.jpg'
                pil_img = Image.open(abs_path).convert('RGB')
                pil_img.save(jpg_path, 'JPEG', quality=self.quality)

                img.filepath = bpy.path.relpath(jpg_path)
                img.reload()
                count += 1
            except Exception as exc:
                self.report({'WARNING'}, f"Lỗi chuyển đổi {img.name}: {exc}")

        self.report({'INFO'}, f"Đã chuyển {count} texture PNG sang JPG ({self.quality}%).")
        return {'FINISHED'}


class SKLUM_OT_convert_selected_image_to_jpg(Operator):
    """Convert ảnh được chọn sang JPG (legacy)"""

    bl_idname = "sklum.convert_selected_image_to_jpg"
    bl_label = "Chuyển Ảnh Được Chọn Sang JPG"
    bl_options = {'REGISTER', 'UNDO'}

    quality: IntProperty(name="Chất lượng JPG", default=95, min=1, max=100)

    def execute(self, context):
        success, message = ensure_pillow_is_installed()
        if not success:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}

        from PIL import Image

        img = context.scene.sklum_jpg_converter_source_image
        if not img:
            self.report({'ERROR'}, "Vui lòng chọn một ảnh.")
            return {'CANCELLED'}

        if img.source != 'FILE' or not img.filepath:
            self.report({'WARNING'}, f"'{img.name}' phải được unpack.")
            return {'CANCELLED'}

        try:
            abs_path = bpy.path.abspath(img.filepath)
            if not os.path.exists(abs_path):
                self.report({'ERROR'}, f"File không tồn tại: {abs_path}")
                return {'CANCELLED'}

            jpg_path = os.path.splitext(abs_path)[0] + '.jpg'
            pil_img = Image.open(abs_path).convert('RGB')
            pil_img.save(jpg_path, 'JPEG', quality=self.quality)

            img.filepath = bpy.path.relpath(jpg_path)
            img.reload()
            self.report({'INFO'}, f"Đã convert '{img.name}' sang JPG ({self.quality}%).")
        except Exception as exc:
            self.report({'ERROR'}, f"Lỗi: {exc}")
            return {'CANCELLED'}

        return {'FINISHED'}


classes = (
    SKLUM_OT_OpenConverterPopup,
    SKLUM_OT_ConverterSelectAll,
    SKLUM_OT_ConverterDeselectAll,
    SKLUM_OT_ConverterRefreshList,
    SKLUM_OT_convert_png_to_jpg_quality,
    SKLUM_OT_convert_selected_image_to_jpg,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
