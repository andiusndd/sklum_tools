"""UI for Object Setting panel"""

import bpy
from bpy.types import Panel

class SKLUM_PT_ObjectSetting(Panel):
    """Bảng cài đặt đối tượng tổng hợp"""
    bl_label = "SKLUM - Object Setting"
    bl_idname = "SKLUM_PT_object_setting"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SKLUM Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # 0. Property Initialization Check
        settings = getattr(scene, "sklum_object_settings", None)
        if not settings:
            layout.label(text="Settings not initialized. Try re-installing.", icon='ERROR')
            return

        # 1. Overlay & Shading (Viewport Access)
        self._draw_overlay_section(layout, context)
        
        # 2. Object Display
        self._draw_object_display_section(layout, context)
        
        # 3. Object Management
        self._draw_object_management_section(layout, context, settings)

    def _draw_overlay_section(self, layout, context):
        # Safe access to space_data properties
        space_data = context.space_data
        if not space_data or space_data.type != 'VIEW_3D':
            return

        overlay = getattr(space_data, "overlay", None)
        shading = getattr(space_data, "shading", None)

        box = layout.box()
        col = box.column(align=True)
        row = col.row()
        row.label(text="Display Overlay", icon='RESTRICT_VIEW_OFF')
        
        if overlay and shading:
            # Row 1: Normal, Wireframes, Random
            row = col.row(align=True)
            row.prop(overlay, "show_face_orientation", text="Normal", icon='NORMALS_FACE')
            row.prop(overlay, "show_wireframes", text="Wireframes", icon='WIRE')
            row.prop_enum(shading, "color_type", value='RANDOM', text="Random")
            
            # Row 2: Flat Color, Origins, render
            row = col.row(align=True)
            row.prop_enum(shading, "light", value='FLAT', text="Flat Color", icon='COLOR')
            row.prop(overlay, "show_object_origins", text="Origins", icon='ORIENTATION_CURSOR')
            row.prop(overlay, "show_overlays", text="render", icon='RENDERLAYERS')
        else:
            col.label(text="Viewport settings inaccessible", icon='ERROR')

    def _draw_object_display_section(self, layout, context):
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Object Display", icon='OBJECT_DATA')
        
        row = col.row(align=True)
        obj = context.active_object
        if obj:
            row.prop_enum(obj, "display_type", 'TEXTURED', text="Default", icon='SHADING_TEXTURE')
            row.prop_enum(obj, "display_type", 'WIRE', text="Wire", icon='SHADING_WIRE')
            row.prop_enum(obj, "display_type", 'BOUNDS', text="Bounds", icon='SHADING_BBOX')
            row.prop(obj, "show_in_front", text="Xray", icon='XRAY')
            row.prop(obj, "show_name", text="Name", icon='SORTALPHA')
        else:
            row.label(text="No active object", icon='INFO')

    def _draw_object_management_section(self, layout, context, settings):
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Object", icon='MESH_DATA')
        
        # Rename
        row = col.row(align=True)
        row.label(text="", icon='QUESTION')
        row.label(text="Rename")
        row.prop(settings, "rename_name", text="")
        row.operator("sklum.object_rename", text="", icon='PLAY')

        # Select By Type
        row = col.row(align=True)
        row.label(text="", icon='RESTRICT_SELECT_OFF')
        row.label(text="Select By Type")
        row.operator("sklum.select_by_type", text="", icon='MESH_ICOSPHERE').type_name = 'MESH'
        row.operator("sklum.select_by_type", text="", icon='LIGHT').type_name = 'LIGHT'
        row.operator("sklum.select_by_type", text="", icon='CAMERA_DATA').type_name = 'CAMERA'
        row.operator("sklum.select_by_type", text="", icon='EMPTY_DATA').type_name = 'EMPTY'
        row.operator("sklum.select_by_type", text="", icon='ARMATURE_DATA').type_name = 'ARMATURE'
        row.operator("sklum.select_by_type", text="", icon='CURVE_DATA').type_name = 'CURVE'

        # Apply Transform
        row = col.row(align=True)
        row.label(text="", icon='MODIFIER')
        row.label(text="Apply Transform")
        row.operator("sklum.apply_transform", text="Scale").mode = 'SCALE'
        row.operator("sklum.apply_transform", text="Rotation").mode = 'ROTATION'
        row.operator("sklum.apply_transform", text="All").mode = 'ALL'

        # Quick Origin
        row = col.row(align=True)
        row.label(text="", icon='ORIENTATION_CURSOR')
        row.label(text="Quick Origin")
        row.operator("sklum.quick_origin", text="Bottom").type = 'BOTTOM'
        row.operator("sklum.quick_origin", text="Center").type = 'CENTER'
        row.operator("sklum.quick_origin", text="Head").type = 'HEAD'

        # Custom Origin
        row = col.row(align=True)
        row.label(text="", icon='ORIENTATION_GIMBAL')
        row.label(text="Custom Origin")
        row.operator("sklum.quick_origin", text="Set").type = 'CUSTOM'
        row.prop(settings, "origin_target_z", text="")
        row.prop(settings, "origin_target_xy", text="")
        row.prop(settings, "origin_target_mode", text="")

        # Shading
        row = col.row(align=True)
        row.label(text="", icon='SETTINGS')
        row.label(text="Shading")
        row.operator("sklum.shading_update", text="FlipNormal").action = 'FLIP'
        row.operator("sklum.shading_update", text="AutoSmooth").action = 'AUTOSMOOTH'
        row.operator("sklum.shading_update", text="MarkSharp").action = 'MARK_SHARP'
        row.operator("sklum.shading_update", text="ClearSharp").action = 'CLEAR_SHARP'

        # Materials
        row = col.row(align=True)
        row.label(text="", icon='MATERIAL')
        row.label(text="Materials")
        row.operator("sklum.material_action", text="Remove").action = 'REMOVE'
        row.operator("sklum.material_action", text="Display").action = 'DISPLAY'
        row.operator("sklum.material_action", text="Rename").action = 'RENAME'

        # Set Location
        row = col.row(align=True)
        row.label(text="", icon='EMPTY_AXIS')
        row.label(text="Set Location")
        row.operator("sklum.set_location", text="Set")
        row.prop(settings, "location_axis", text="")
        row.prop(settings, "location_value", text="")

        # Parent
        row = col.row(align=True)
        row.label(text="", icon='ORIENTATION_PARENT')
        row.label(text="Parent")
        row.operator("sklum.parent_action", text="Set").action = 'SET'
        row.operator("sklum.parent_action", text="Clear").action = 'CLEAR'

        # Final Big Button
        layout.separator()
        layout.operator("object.make_single_user", text="Make Single User", icon='QUESTION').type = 'ALL'


classes = (
    SKLUM_PT_ObjectSetting,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
