"""Panel UI for SKLUM - Import/Export"""

import bpy
from bpy.types import Panel


class VIEW3D_PT_sklum_import_export(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SKLUM Tools'
    bl_label = "SKLUM - Import/Export"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row(align=True)
        row.operator("sklum.import_material_glb", text="Import .GLB Material", icon='IMPORT')

        row = layout.row(align=True)
        row.operator("sklum.export_glb", text="Export .GLB", icon='EXPORT')

        row = layout.row(align=True)
        row.operator("sklum.pack_textures", text="Pack Textures", icon='PACKAGE')
        row.operator("sklum.unpack_all_textures", text="Unpack Textures", icon='FILE_FOLDER')

        row = layout.row(align=True)
        row.operator("sklum.purge_unused", text="Purge Unused", icon='TRASH')

        layout.separator()

        # GLB Compression workflow
        box = layout.box()
        box.label(text="GLB Compression (Draco/KTX2)", icon='MOD_MESHDEFORM')
        row = box.row()
        row.operator("sklum.open_gltf_compressor", text="Open Khronos Compressor", icon='URL')

classes = (VIEW3D_PT_sklum_import_export,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
