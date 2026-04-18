import bpy


class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.add_filename"
    bl_label = "FileName追加"

    def execute(self, context):
        context.object["file_name"] = ""
        return {"FINISHED"}
