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

    def _draw_split_row(self, layout, label, icon, factor=0.4):
        """Helper to draw consistent split row: Label (40%) | Buttons (60%)"""
        split = layout.split(factor=factor, align=True)
        col_label = split.column(align=True)
        col_label.alignment = 'LEFT'
        col_label.label(text=label, icon=icon)
        return split.column(align=True)

    def _draw_overlay_section(self, layout, context):
        # Safe access to space_data properties
        space_data = context.space_data
        if not space_data or space_data.type != 'VIEW_3D':
            return

        overlay = getattr(space_data, "overlay", None)
        shading = getattr(space_data, "shading", None)

        box = layout.box()
        col = box.column(align=True)
        col.label(text="Display Overlay", icon='RESTRICT_VIEW_OFF')
        
        if overlay and shading:
            # Row 1: Normal | Wireframes | Random
            row = col.row(align=True)
            row.prop(overlay, "show_face_orientation", text="Normal", icon='NORMALS_FACE', toggle=True)
            row.prop(overlay, "show_wireframes", text="Wireframes", icon='SHADING_WIRE', toggle=True)
            row.prop_enum(shading, "color_type", value='RANDOM', text="Random", icon='SHADING_BBOX') # Icon approx

            # Row 2: Flat Color | Origins | render
            row = col.row(align=True)
            row.prop_enum(shading, "light", value='FLAT', text="Flat Color", icon='COLOR')
            row.prop(overlay, "show_object_origins", text="Origins", icon='ORIENTATION_CURSOR', toggle=True)
            row.prop(overlay, "show_overlays", text="render", icon='RENDERLAYERS', toggle=True)
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
            row.prop(obj, "show_in_front", text="Xray", icon='XRAY', toggle=True)
            row.prop(obj, "show_name", text="Name", icon='SORTALPHA', toggle=True)
        else:
            row.label(text="No active object", icon='INFO')

    def _draw_object_management_section(self, layout, context, settings):
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Object", icon='MESH_DATA')
        
        # Rename
        right = self._draw_split_row(col, "Rename", 'QUESTION')
        row = right.row(align=True)
        row.prop(settings, "rename_name", text="")
        row.operator("sklum.object_rename", text="", icon='PLAY')

        # Select By Type
        right = self._draw_split_row(col, "Select By Type", 'RESTRICT_SELECT_OFF')
        row = right.row(align=True)
        row.operator("sklum.select_by_type", text="", icon='MESH_ICOSPHERE').type_name = 'MESH'
        row.operator("sklum.select_by_type", text="", icon='LIGHT').type_name = 'LIGHT'
        row.operator("sklum.select_by_type", text="", icon='CAMERA_DATA').type_name = 'CAMERA'
        row.operator("sklum.select_by_type", text="", icon='CURVE_DATA').type_name = 'CURVE'
        row.operator("sklum.select_by_type", text="", icon='EMPTY_DATA').type_name = 'EMPTY'
        row.operator("sklum.select_by_type", text="", icon='ARMATURE_DATA').type_name = 'ARMATURE'
        row.operator("sklum.select_by_type", text="", icon='NODE').type_name = 'LATTICE' # Heuristic

        # Apply Transform
        right = self._draw_split_row(col, "Apply Transform", 'MODIFIER')
        row = right.row(align=True)
        row.operator("sklum.apply_transform", text="Scale").mode = 'SCALE'
        row.operator("sklum.apply_transform", text="Rotation").mode = 'ROTATION'
        row.operator("sklum.apply_transform", text="All").mode = 'ALL'

        # Quick Origin
        right = self._draw_split_row(col, "Quick Origin", 'ORIENTATION_CURSOR')
        row = right.row(align=True)
        row.operator("sklum.quick_origin", text="Bottom").type = 'BOTTOM'
        row.operator("sklum.quick_origin", text="Center").type = 'CENTER'
        row.operator("sklum.quick_origin", text="Head").type = 'HEAD'

        # Custom Origin
        right = self._draw_split_row(col, "Custom Origin", 'ORIENTATION_GIMBAL')
        row = right.row(align=True)
        row.operator("sklum.quick_origin", text="Set").type = 'CUSTOM'
        row.prop(settings, "origin_target_z", text="")
        row.prop(settings, "origin_target_xy", text="")
        row.prop(settings, "origin_target_mode", text="")

        # Shading
        right = self._draw_split_row(col, "Shading", 'SETTINGS')
        row = right.row(align=True)
        row.operator("sklum.shading_update", text="FlipN").action = 'FLIP'
        row.operator("sklum.shading_update", text="AutoS").action = 'AUTOSMOOTH'
        row.operator("sklum.shading_update", text="Mark").action = 'MARK_SHARP'
        row.operator("sklum.shading_update", text="Clear").action = 'CLEAR_SHARP'

        # Materials
        right = self._draw_split_row(col, "Materials", 'MATERIAL')
        row = right.row(align=True)
        row.operator("sklum.material_action", text="Remove").action = 'REMOVE'
        row.operator("sklum.material_action", text="Display").action = 'DISPLAY'
        row.operator("sklum.material_action", text="Rename").action = 'RENAME'

        # Set Location
        right = self._draw_split_row(col, "Set Location", 'EMPTY_AXIS')
        row = right.row(align=True)
        row.operator("sklum.set_location", text="Set")
        row.prop(settings, "location_axis", text="")
        row.prop(settings, "location_value", text="")

        # Parent
        right = self._draw_split_row(col, "Parent", 'ORIENTATION_PARENT')
        row = right.row(align=True)
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
