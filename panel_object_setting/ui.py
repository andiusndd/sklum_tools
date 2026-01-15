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
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        """Only show this panel if license is active"""
        return context.scene.sklum_license_active

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
        space_data = context.space_data
        if not space_data or space_data.type != 'VIEW_3D':
            return

        overlay = getattr(space_data, "overlay", None)
        shading = getattr(space_data, "shading", None)

        box = layout.box()
        col = box.column(align=True)
        col.label(text="Hiển thị Overlay", icon='RESTRICT_VIEW_OFF')
        
        if overlay and shading:
            # Row 1: Normal | Wireframes | Random (Toggle Operator)
            row = col.row(align=True)
            row.prop(overlay, "show_face_orientation", text="Normal", icon='NORMALS_FACE', toggle=True)
            row.prop(overlay, "show_wireframes", text="Lưới (Wire)", icon='SHADING_WIRE', toggle=True)
            
            # Random Toggle
            is_random = (shading.color_type == 'RANDOM')
            row.operator("sklum.toggle_color", text="Màu Ngẫu nhiên", icon='SHADING_BBOX', depress=is_random)

            # Row 2: Flat Color (Toggle) | Origins | Render (Inverted Fix)
            row = col.row(align=True)
            
            # Flat Toggle
            is_flat = (shading.light == 'FLAT')
            row.operator("sklum.toggle_light", text="Màu Phẳng", icon='COLOR', depress=is_flat)
            
            row.prop(overlay, "show_object_origins", text="Gốc (Origins)", icon='ORIENTATION_CURSOR', toggle=True)
            
            # Render Button (Inverted Logic: Show Render = Hide Overlays)
            # Text "Render" implies Clean View -> show_overlays = False
            # So if show_overlays is False, button should be ON (depressed)
            is_render_clean = not overlay.show_overlays
            op = row.operator("wm.context_toggle", text="Render (Sạch)", icon='RENDERLAYERS', depress=is_render_clean)
            op.data_path = "space_data.overlay.show_overlays" 

    def _draw_object_display_section(self, layout, context):
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Hiển thị Đối tượng", icon='OBJECT_DATA')
        
        row = col.row(align=True)
        obj = context.active_object
        if obj:
            row.prop_enum(obj, "display_type", 'TEXTURED', text="Mặc định", icon='SHADING_TEXTURE')
            row.prop_enum(obj, "display_type", 'WIRE', text="Lưới", icon='SHADING_WIRE')
            row.prop_enum(obj, "display_type", 'BOUNDS', text="Khung", icon='SHADING_BBOX')
            row.prop(obj, "show_in_front", text="Xray", icon='XRAY', toggle=True)
            row.prop(obj, "show_name", text="Tên", icon='SORTALPHA', toggle=True)
        else:
            row.label(text="Chưa chọn đối tượng", icon='INFO')

    def _draw_vertical_group(self, layout, label, icon):
        col = layout.column(align=True)
        col.label(text=label, icon=icon)
        return col

    def _draw_object_management_section(self, layout, context, settings):
        layout.separator()
        layout.label(text="Quản lý Đối tượng", icon='MESH_DATA')
        
        # 0. Objects Gizmos (NEW)
        col = self._draw_vertical_group(layout, "Trục điều khiển (Gizmos)", 'GIZMO')
        row = col.row(align=True)
        
        space = context.space_data
        
        # Move
        is_move = space.show_gizmo_object_translate
        row.operator("sklum.toggle_gizmo", text="Di chuyển", icon='GIZMO', depress=is_move).type = 'TRANSLATE'
        
        # Rotate
        is_rotate = space.show_gizmo_object_rotate
        row.operator("sklum.toggle_gizmo", text="Xoay", icon='DRIVER_ROTATIONAL_DIFFERENCE', depress=is_rotate).type = 'ROTATE'
        
        # Scale
        is_scale = space.show_gizmo_object_scale
        row.operator("sklum.toggle_gizmo", text="Phóng to", icon='FULLSCREEN_ENTER', depress=is_scale).type = 'SCALE'


        # 1. Rename
        col = self._draw_vertical_group(layout, "Đổi tên (Rename)", 'QUESTION')
        row = col.row(align=True)
        row.prop(settings, "rename_name", text="")
        row.operator("sklum.object_rename", text="Đổi tên", icon='PLAY')

        # 2. Select By Type (Grid 3 cols)
        col = self._draw_vertical_group(layout, "Chọn theo loại", 'RESTRICT_SELECT_OFF')
        grid = col.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=True)
        grid.operator("sklum.select_by_type", text="Mesh", icon='MESH_ICOSPHERE').type_name = 'MESH'
        grid.operator("sklum.select_by_type", text="Đèn", icon='LIGHT').type_name = 'LIGHT'
        grid.operator("sklum.select_by_type", text="Camera", icon='CAMERA_DATA').type_name = 'CAMERA'
        grid.operator("sklum.select_by_type", text="Curve", icon='CURVE_DATA').type_name = 'CURVE'
        grid.operator("sklum.select_by_type", text="Empty", icon='EMPTY_DATA').type_name = 'EMPTY'
        grid.operator("sklum.select_by_type", text="Xương", icon='ARMATURE_DATA').type_name = 'ARMATURE'
        
        # 3. Apply Transform (Row)
        col = self._draw_vertical_group(layout, "Áp dụng biến đổi (Apply)", 'MODIFIER')
        row = col.row(align=True)
        row.operator("sklum.apply_transform", text="Scale").mode = 'SCALE'
        row.operator("sklum.apply_transform", text="Xoay").mode = 'ROTATION'
        row.operator("sklum.apply_transform", text="Tất cả").mode = 'ALL'

        # 4. Quick Origin (Row)
        col = self._draw_vertical_group(layout, "Tâm nhanh (Quick Origin)", 'ORIENTATION_CURSOR')
        row = col.row(align=True)
        row.operator("sklum.quick_origin", text="Dưới đáy").type = 'BOTTOM'
        row.operator("sklum.quick_origin", text="Trọng tâm").type = 'CENTER'
        row.operator("sklum.quick_origin", text="Trên đỉnh").type = 'HEAD'

        # 5. Custom Origin (Row complex)
        col = self._draw_vertical_group(layout, "Tâm tùy chọn (Custom Origin)", 'ORIENTATION_GIMBAL')
        row = col.row(align=True)
        row.scale_y = 1.2
        row.operator("sklum.quick_origin", text="Đặt tâm theo tùy chọn bên dưới").type = 'CUSTOM'
        
        # X Axis Alignment
        row = col.row(align=True)
        row.label(text="X:")
        row.prop(settings, "origin_align_x", expand=True)
        
        # Y Axis Alignment
        row = col.row(align=True)
        row.label(text="Y:")
        row.prop(settings, "origin_align_y", expand=True)
        
        # Z Axis Alignment
        row = col.row(align=True)
        row.label(text="Z:")
        row.prop(settings, "origin_align_z", expand=True)

        # 6. Shading (Grid 2 cols)
        col = self._draw_vertical_group(layout, "Shading", 'SETTINGS')
        grid = col.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
        grid.operator("sklum.shading_update", text="Lật Normal").action = 'FLIP'
        grid.operator("sklum.shading_update", text="Auto Smooth").action = 'AUTOSMOOTH'
        grid.operator("sklum.shading_update", text="Mark Sharp").action = 'MARK_SHARP'
        grid.operator("sklum.shading_update", text="Clear Sharp").action = 'CLEAR_SHARP'

        # 7. Materials (Row)
        col = self._draw_vertical_group(layout, "Vật liệu (Materials)", 'MATERIAL')
        row = col.row(align=True)
        row.operator("sklum.material_action", text="Xóa Slot").action = 'REMOVE'
        row.operator("sklum.material_action", text="Hiển thị").action = 'DISPLAY'
        row.operator("sklum.material_action", text="Đổi tên").action = 'RENAME'

        # 8. Set Location
        col = self._draw_vertical_group(layout, "Đặt vị trí (Location)", 'EMPTY_AXIS')
        row = col.row(align=True)
        row.operator("sklum.set_location", text="Đặt")
        row.prop(settings, "location_axis", text="")
        row.prop(settings, "location_value", text="")

        # 9. Parent
        col = self._draw_vertical_group(layout, "Liên kết (Parent)", 'ORIENTATION_PARENT')
        row = col.row(align=True)
        row.operator("sklum.parent_action", text="Set Parent").action = 'SET'
        row.operator("sklum.parent_action", text="Clear Parent").action = 'CLEAR'

        # 10. Final
        layout.separator()
        layout.operator("object.make_single_user", text="Tách rời (Make Single User)", icon='QUESTION').type = 'ALL'


classes = (
    SKLUM_PT_ObjectSetting,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
