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

    def _draw_vertical_group(self, layout, label, icon):
        """Helper: Group Name (Row) -> Content (Row via grid/column)"""
        col = layout.column(align=True)
        col.label(text=label, icon=icon)
        return col

    def _draw_object_management_section(self, layout, context, settings):
        layout.separator()
        layout.label(text="Object Management", icon='MESH_DATA')
        
        # 1. Rename
        col = self._draw_vertical_group(layout, "Rename", 'QUESTION')
        row = col.row(align=True)
        row.prop(settings, "rename_name", text="")
        row.operator("sklum.object_rename", text="Rename", icon='PLAY')

        # 2. Select By Type (Grid 3 cols)
        col = self._draw_vertical_group(layout, "Select By Type", 'RESTRICT_SELECT_OFF')
        grid = col.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=True)
        grid.operator("sklum.select_by_type", text="Mesh", icon='MESH_ICOSPHERE').type_name = 'MESH'
        grid.operator("sklum.select_by_type", text="Light", icon='LIGHT').type_name = 'LIGHT'
        grid.operator("sklum.select_by_type", text="Camera", icon='CAMERA_DATA').type_name = 'CAMERA'
        grid.operator("sklum.select_by_type", text="Curve", icon='CURVE_DATA').type_name = 'CURVE'
        grid.operator("sklum.select_by_type", text="Empty", icon='EMPTY_DATA').type_name = 'EMPTY'
        grid.operator("sklum.select_by_type", text="Armature", icon='ARMATURE_DATA').type_name = 'ARMATURE'
        
        # 3. Apply Transform (Row)
        col = self._draw_vertical_group(layout, "Apply Transform", 'MODIFIER')
        row = col.row(align=True)
        row.operator("sklum.apply_transform", text="Scale").mode = 'SCALE'
        row.operator("sklum.apply_transform", text="Rotation").mode = 'ROTATION'
        row.operator("sklum.apply_transform", text="All").mode = 'ALL'

        # 4. Quick Origin (Row)
        col = self._draw_vertical_group(layout, "Quick Origin", 'ORIENTATION_CURSOR')
        row = col.row(align=True)
        row.operator("sklum.quick_origin", text="Bottom").type = 'BOTTOM'
        row.operator("sklum.quick_origin", text="Center").type = 'CENTER'
        row.operator("sklum.quick_origin", text="Head").type = 'HEAD'

        # 5. Custom Origin (Row complex)
        col = self._draw_vertical_group(layout, "Custom Origin", 'ORIENTATION_GIMBAL')
        row = col.row(align=True)
        row.scale_y = 1.2
        row.operator("sklum.quick_origin", text="Set Origin to Custom Alignment").type = 'CUSTOM'
        
        # Grid for X Y Z
        grid = col.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=True)
        grid.prop(settings, "origin_align_x", text="")
        grid.prop(settings, "origin_align_y", text="")
        grid.prop(settings, "origin_align_z", text="")

        # 6. Shading (Grid 2 cols)
        col = self._draw_vertical_group(layout, "Shading", 'SETTINGS')
        grid = col.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
        grid.operator("sklum.shading_update", text="Flip Normal").action = 'FLIP'
        grid.operator("sklum.shading_update", text="Auto Smooth").action = 'AUTOSMOOTH'
        grid.operator("sklum.shading_update", text="Mark Sharp").action = 'MARK_SHARP'
        grid.operator("sklum.shading_update", text="Clear Sharp").action = 'CLEAR_SHARP'

        # 7. Materials (Row)
        col = self._draw_vertical_group(layout, "Materials", 'MATERIAL')
        row = col.row(align=True)
        row.operator("sklum.material_action", text="Remove").action = 'REMOVE'
        row.operator("sklum.material_action", text="Display").action = 'DISPLAY'
        row.operator("sklum.material_action", text="Rename").action = 'RENAME'

        # 8. Set Location
        col = self._draw_vertical_group(layout, "Set Location", 'EMPTY_AXIS')
        row = col.row(align=True)
        row.operator("sklum.set_location", text="Set")
        row.prop(settings, "location_axis", text="")
        row.prop(settings, "location_value", text="")

        # 9. Parent
        col = self._draw_vertical_group(layout, "Parent", 'ORIENTATION_PARENT')
        row = col.row(align=True)
        row.operator("sklum.parent_action", text="Set Parent").action = 'SET'
        row.operator("sklum.parent_action", text="Clear Parent").action = 'CLEAR'

        # 10. Final
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
