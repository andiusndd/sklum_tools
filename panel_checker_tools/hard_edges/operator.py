"""Select hard edges operator"""

import bpy
import bmesh
from math import degrees
from bpy.types import Operator


class SKLUM_OT_select_hard_edges(Operator):
    """Select edges with an angle greater than the specified threshold"""
    bl_idname = "sklum.select_hard_edges"
    bl_label = "Select Hard Edges"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'MESH'
            and context.mode in {'OBJECT', 'EDIT_MESH'}
        )

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='EDIT')

        obj = context.active_object
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)

        angle_limit = context.scene.sklum_sharpness_angle

        bm.edges.ensure_lookup_table()
        for edge in bm.edges:
            if not edge.is_boundary and degrees(edge.calc_face_angle()) > angle_limit:
                edge.select = True
            else:
                edge.select = False

        bmesh.update_edit_mesh(mesh)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SKLUM_OT_select_hard_edges)


def unregister():
    bpy.utils.unregister_class(SKLUM_OT_select_hard_edges)
