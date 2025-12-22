"""Menus cho preset Auto Rename"""

import bpy
from bpy.types import Menu

from .operators import SKLUM_OT_SetPresetValue
from . import utils


class SKLUM_MT_PresetMenuBase(Menu):
    """Menu cơ bản cho các preset"""

    bl_label = "Presets"
    preset_type = ""
    target_prop = ""
    target_context = "sklum_auto_rename_settings"

    def draw(self, context):
        layout = self.layout
        presets = utils.load_presets()
        items = presets.get(self.preset_type, [])

        for value in items:
            op = layout.operator(SKLUM_OT_SetPresetValue.bl_idname, text=value)
            op.value = value
            op.target_prop = self.target_prop
            op.target_context = self.target_context


class SKLUM_MT_ModelTypePresets(SKLUM_MT_PresetMenuBase):
    bl_idname = "SKLUM_MT_model_type_presets"
    bl_label = "Model Type Presets"
    preset_type = "model_types"
    target_prop = "model_type"


class SKLUM_MT_MainMaterialPresets(SKLUM_MT_PresetMenuBase):
    bl_idname = "SKLUM_MT_main_material_presets"
    bl_label = "Collection Presets"
    preset_type = "main_materials"
    target_prop = "main_material"


class SKLUM_MT_MeshNamePresets(SKLUM_MT_PresetMenuBase):
    bl_idname = "SKLUM_MT_mesh_name_presets"
    bl_label = "Mesh Name Presets"
    preset_type = "mesh_names"
    target_prop = "mesh_name"


class SKLUM_MT_MaterialNamePresets(SKLUM_MT_PresetMenuBase):
    bl_idname = "SKLUM_MT_material_name_presets"
    bl_label = "Material Name Presets"
    preset_type = "material_names"
    target_prop = "material_name"


classes = (
    SKLUM_MT_ModelTypePresets,
    SKLUM_MT_MainMaterialPresets,
    SKLUM_MT_MeshNamePresets,
    SKLUM_MT_MaterialNamePresets,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
