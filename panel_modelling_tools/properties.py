import bpy
from bpy.props import BoolProperty, PointerProperty

class ModellingToolsProperties(bpy.types.PropertyGroup):
    # UI Control
    show_basic_tools: BoolProperty(
        name="Basic Modelling",
        description="Show/Hide basic modelling tools",
        default=True
    )
    show_advanced_tools: BoolProperty(
        name="Advanced Modelling",
        description="Show/Hide advanced modelling tools",
        default=True
    )
    
    # Tool specific settings could go here

def register():
    bpy.utils.register_class(ModellingToolsProperties)
    bpy.types.Scene.modelling_tools = PointerProperty(type=ModellingToolsProperties)

def unregister():
    del bpy.types.Scene.modelling_tools
    bpy.utils.unregister_class(ModellingToolsProperties)
