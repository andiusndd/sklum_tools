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


def get_furniture_items(self, context):
    """Returns 100 furniture items sorted A-Z for model_type dropdown."""
    furniture_list = [
        "Armchair", "Basin", "Bed", "Bench", "Bin", "Blanket", "Blender", "Blinds",
        "Bookshelf", "Bowl", "Broom", "Brush", "Bucket", "Bulb", "Cabinet", "Candle",
        "Canister", "Carpet", "Chair", "Chandelier", "Closet", "Clock", "Comb", "Comforter",
        "Cot", "Couch", "Cradle", "Cup", "Cupboard", "Curtains", "Cushion", "Desk",
        "Dish", "Drapes", "Dresser", "Dryer", "Duvet", "Fan", "Faucet", "Fork",
        "Frame", "Freezer", "Fridge", "Futon", "Glass", "Hammock", "Heater", "Iron",
        "Jar", "Jug", "Kettle", "Knife", "Ladle", "Lamp", "Lantern", "Mat",
        "Mattress", "Microwave", "Mirror", "Mixer", "Mop", "Mug", "Nightstand", "Ottoman",
        "Oven", "Painting", "Pan", "Photo", "Pillow", "Pitcher", "Plant", "Plate",
        "Poster", "Pot", "Quilt", "Recliner", "Rug", "Shelf", "Sheet", "Shower",
        "Sideboard", "Sink", "Soap", "Sofa", "Sponge", "Spoon", "Statue", "Stool",
        "Stove", "Table", "Tap", "Toaster", "Toilet", "Towel", "Tray", "Tub",
        "Vase", "Wardrobe", "Washer", "Wok"
    ]
    
    # Return as enum items: (identifier, name, description)
    return [(item, item, f"Furniture type: {item}") for item in furniture_list]


def get_material_items(self, context):
    """Returns 34 material items for material_name dropdown (from material.csv)."""
    material_list = [
        "Solidwood", "Hardwood", "Softwood", "Plywood", "MDF", "Veneer", "Bamboo",
        "Rattan", "Steel", "Stainless steel", "Aluminum", "Iron", "Wrought iron",
        "Brass", "Copper", "Tempered glass", "Marble", "Granite", "Quartz", "Ceramic",
        "Concrete", "Leather", "Faux leather", "Velvet", "Linen", "Cotton", "Polyester",
        "Silk", "Wool", "Plastic", "Acrylic", "Resin", "Rubber", "Foam"
    ]
    
    # Return as enum items: (identifier, name, description)
    return [(item, item, f"Material: {item}") for item in material_list]


def get_mesh_name_items(self, context):
    """Returns mesh name items filtered by selected model_type.
    
    This callback dynamically filters parts based on the furniture type
    selected in model_type field.
    """
    # Get the current model_type from parent settings
    settings = context.scene.sklum_auto_rename_settings
    model_type = settings.model_type
    
    if model_type:
        # Get parts for this specific model type
        parts = utils.get_parts_for_model(model_type)
    else:
        # No model type selected, show default
        parts = ['Part']
    
    # Return as enum items: (identifier, name, description)
    return [(part, part, f"Part: {part}") for part in parts]


class SKLUM_PG_AutoRenameItem(PropertyGroup):
    original_name: StringProperty()
    mesh_name: EnumProperty(
        name="Tên",
        items=get_mesh_name_items,
        description="Select part name (filtered by model type)"
    )
    material_name: EnumProperty(
        name="Tên VL",
        items=get_material_items,
        description="Select material type from preset list"
    )


class SKLUM_PG_AutoRenameSettings(PropertyGroup):
    model_id: StringProperty(
        name="Model ID",
        update=lambda self, context: self.update_idp_and_collection_from_model_id(context),
    )
    idp: StringProperty(name="IDP")
    model_type: EnumProperty(
        name="Loại Model",
        items=get_furniture_items,
        description="Select furniture type from preset list"
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
