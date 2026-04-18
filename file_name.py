import bpy


class OBJECT_PT_file_name(bpy.types.Panel):
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        obj = context.object
        layout = self.layout

        if obj is None:
            return

        if "file_name" in obj:
            layout.prop(obj, '["file_name"]')
        else:
            layout.operator("myaddon.add_filename")
