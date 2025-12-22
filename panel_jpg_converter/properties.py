"""Scene properties cho panel JPG Converter"""

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    StringProperty,
    IntProperty,
    BoolProperty,
    CollectionProperty,
    PointerProperty,
)


class SKLUM_PG_ConverterTextureItem(PropertyGroup):
    """Item đại diện cho một texture PNG trong danh sách convert"""

    image_name: StringProperty(
        name="Image Name",
        description="Tên ảnh trong Blender",
    )

    filepath: StringProperty(
        name="File Path",
        description="Đường dẫn tuyệt đối đến file",
    )

    enabled: BoolProperty(
        name="Enabled",
        description="Bật/tắt convert texture này",
        default=True,
    )

    use_custom_quality: BoolProperty(
        name="Custom Quality",
        description="Sử dụng chất lượng riêng thay vì global",
        default=False,
    )

    quality: IntProperty(
        name="Quality",
        description="Chất lượng JPG (1-100)",
        default=95,
        min=1,
        max=100,
        subtype='PERCENTAGE',
    )


class SKLUM_PG_ConverterSettings(PropertyGroup):
    """Settings tổng cho converter popup"""

    global_quality: IntProperty(
        name="Global Quality",
        description="Chất lượng JPG áp dụng cho tất cả textures",
        default=95,
        min=1,
        max=100,
        subtype='PERCENTAGE',
    )

    items: CollectionProperty(
        type=SKLUM_PG_ConverterTextureItem,
        name="Texture Items",
    )

    active_index: IntProperty(
        name="Active Index",
        default=0,
    )

    delete_png_after: BoolProperty(
        name="Delete PNG",
        description="Xóa file PNG gốc sau khi convert",
        default=False,
    )


classes = (
    SKLUM_PG_ConverterTextureItem,
    SKLUM_PG_ConverterSettings,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Legacy property for backward compatibility
    bpy.types.Scene.sklum_jpg_converter_source_image = PointerProperty(
        type=bpy.types.Image,
        name="Source Image",
        description="Chọn ảnh để chuyển đổi sang JPG",
    )

    # New converter settings
    bpy.types.Scene.sklum_converter_settings = PointerProperty(
        type=SKLUM_PG_ConverterSettings,
    )


def unregister():
    if hasattr(bpy.types.Scene, 'sklum_converter_settings'):
        del bpy.types.Scene.sklum_converter_settings

    if hasattr(bpy.types.Scene, 'sklum_jpg_converter_source_image'):
        del bpy.types.Scene.sklum_jpg_converter_source_image

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
