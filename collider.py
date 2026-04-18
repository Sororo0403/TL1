import bpy


class OBJECT_PT_collider(bpy.types.Panel):
    bl_label = "Collider"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        obj = context.object
        layout = self.layout

        if obj is None:
            return

        if "collider" in obj:
            layout.prop(obj, '["collider"]')
            layout.prop(obj, '["collider_center"]')
            layout.prop(obj, '["collider_size"]')
        else:
            layout.operator("myaddon.add_collider")
