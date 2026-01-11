"""Property groups cho Auto Rename"""

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    StringProperty,
    EnumProperty,
    CollectionProperty,
    PointerProperty,
    IntProperty,
)

from . import utils


def search_furniture_items(self, context, edit_text):
    """Search callback for model_type StringProperty."""
    return [item for item in utils.FURNITURE_DATA if edit_text.lower() in item.lower()]


def search_material_items(self, context, edit_text):
    """Search callback for material_name StringProperty."""
    return [item for item in utils.MATERIAL_DATA if edit_text.lower() in item.lower()]


def search_mesh_name_items(self, context, edit_text):
    """Search callback for mesh_name StringProperty (dynamic filtering)."""
    # Get the current model_type from parent settings
    settings = context.scene.sklum_auto_rename_settings
    model_type = settings.model_type
    
    if model_type:
        parts = utils.get_parts_for_model(model_type)
    else:
        parts = ['Part']
    
    return [part for part in parts if edit_text.lower() in part.lower()]


class SKLUM_PG_AutoRenameItem(PropertyGroup):
    original_name: StringProperty()
    mesh_name: StringProperty(
        name="Tên",
        search=search_mesh_name_items,
        description="Select part name (filtered by model type) or type manually"
    )
    material_name: StringProperty(
        name="Tên VL",
        search=search_material_items,
        description="Select material type or type manually"
    )


class SKLUM_PG_AutoRenameSettings(PropertyGroup):
    model_id: StringProperty(
        name="Model ID",
        update=lambda self, context: self.update_idp_and_collection_from_model_id(context),
    )
    idp: StringProperty(name="IDP")
    model_type: StringProperty(
        name="Loại Model",
        search=search_furniture_items,
        description="Select furniture type or type manually"
    )
    main_material: StringProperty(name="Collection")

    csv_filepath: StringProperty(
        name="CSV File",
        subtype="FILE_PATH",
        description="Đường dẫn đến file CSV chứa dữ liệu IDP và Collection",
        update=utils.update_and_load_csv,
    )

    items: CollectionProperty(type=SKLUM_PG_AutoRenameItem)
    active_index: IntProperty(
        name="Active Index",
        default=0,
        update=lambda self, context: self.update_active_object(context),
    )

    def update_idp_and_collection_from_model_id(self, context):
        info = utils.get_idp_info(self.model_id)
        if info:
            self.idp = info['idp']
            self.main_material = info['collection']
        else:
            self.idp = ""
            self.main_material = ""

    def update_active_object(self, context):
        if context.mode == 'OBJECT' and bpy.ops.object.select_all.poll():
            bpy.ops.object.select_all(action='DESELECT')

        if self.active_index < 0 or self.active_index >= len(self.items):
            return

        selected_item = self.items[self.active_index]
        obj = context.scene.objects.get(selected_item.original_name) or context.scene.objects.get(selected_item.mesh_name)
        if obj:
            obj.select_set(True)
            context.view_layer.objects.active = obj


classes = (
    SKLUM_PG_AutoRenameItem,
    SKLUM_PG_AutoRenameSettings,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.sklum_auto_rename_settings = PointerProperty(type=SKLUM_PG_AutoRenameSettings)


def unregister():
    del bpy.types.Scene.sklum_auto_rename_settings

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
