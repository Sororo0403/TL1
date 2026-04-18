import bpy
from mathutils import Vector


class MYADDON_OT_add_collider(bpy.types.Operator):
    bl_idname = "myaddon.add_collider"
    bl_label = "コライダー追加"

    def execute(self, context):
        obj = context.object
        obj["collider"] = "BOX"
        obj["collider_center"] = Vector((0, 0, 0))
        obj["collider_size"] = Vector((2, 2, 2))
        return {"FINISHED"}
