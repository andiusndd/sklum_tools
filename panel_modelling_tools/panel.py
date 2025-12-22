import bpy
from bpy.types import Panel

class VIEW3D_PT_sklum_modelling(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SKLUM Tools'
    bl_label = "SKLUM - Modelling Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.modelling_tools

        # --- PART 1: BASIC MODELLING ---
        box = layout.box()
        row = box.row()
        row.prop(
            props,
            "show_basic_tools",
            icon="TRIA_DOWN" if props.show_basic_tools else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        row.label(text="CƠ BẢN (Basic Modelling)", icon='MESH_CUBE')
        
        if props.show_basic_tools:
            # Pivot Tools
            col = box.column(align=True)
            col.label(text="Pivot Master:", icon='PIVOT_CURSOR')
            row = col.row(align=True)
            row.operator("modelling.floor_it", text="Floor It", icon='ANCHOR_CENTER')
            row.operator("modelling.pivot_to_zero", text="Origin to Zero", icon='WORLD')
            
            row = col.row(align=True)
            op = row.operator("modelling.nine_point_pivot", text="Pivot: Bottom", icon='DOT')
            op.point = 'BOTTOM_CENTER'
            op = row.operator("modelling.nine_point_pivot", text="Center", icon='DOT')
            op.point = 'CENTER'
            op = row.operator("modelling.nine_point_pivot", text="Top", icon='DOT')
            op.point = 'TOP_CENTER'
            
            box.separator()
            
            # Mesh Quick-Fix
            col = box.column(align=True)
            col.label(text="Mesh Quick-Fix:", icon='BRUSH_DATA')
            row = col.row(align=True)
            row.operator("modelling.delete_interior", text="Delete Interior", icon='MOD_SOLIDIFY')
            row.operator("modelling.quick_cleanup", text="Quick Cleanup", icon='MODIFIER')
            
            box.separator()
            
            # Shading
            col = box.column(align=True)
            col.label(text="Standard Shading:", icon='SHADING_SOLID')
            col.operator("modelling.auto_smooth", text="Auto Smooth Setup", icon='MOD_SMOOTH')

        layout.separator()

        # --- PART 2: ADVANCED MODELLING ---
        box = layout.box()
        row = box.row()
        row.prop(
            props,
            "show_advanced_tools",
            icon="TRIA_DOWN" if props.show_advanced_tools else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        row.label(text="NÂNG CAO (Advanced Modelling)", icon='MODIFIER')

        if props.show_advanced_tools:
            # Technical Dimensions
            col = box.column(align=True)
            col.label(text="Technical Dimensions (Ghost Bounds):", icon='OBJECT_DATA')
            col.operator("modelling.create_ghost_bounds", text="Create Ghost Bounds", icon='MOD_WIREFRAME')
            
            box.separator()

            # Advanced Pivot
            col = box.column(align=True)
            col.label(text="Advanced Pivot Suite:", icon='PIVOT_ACTIVE')
            col.operator("modelling.align_to_active", text="Align Pivot to Active", icon='CONSTRAINT')
            
            box.separator()
            
            # Pro Shading & Geometry
            col = box.column(align=True)
            col.label(text="Pro Shading & Geometry:", icon='MOD_NORMALEDIT')
            col.operator("modelling.smart_hardener", text="Smart Hardener (W.Normal)", icon='MOD_EDGESPLIT')
            col.operator("modelling.planar_snap", text="Planar Snap (Flatten)", icon='MOD_BUILD')

def register():
    bpy.utils.register_class(VIEW3D_PT_sklum_modelling)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_sklum_modelling)
