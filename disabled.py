import bpy


class MYADDON_OT_add_disabled(bpy.types.Operator):
    bl_idname = "myaddon.add_disabled"
    bl_label = "Add Disabled"
    bl_description = "オブジェクトに無効フラグを追加"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.object

        if obj is None:
            self.report({"WARNING"}, "オブジェクトが選択されていません")
            return {"CANCELLED"}

        obj["disabled"] = True

        return {"FINISHED"}


class OBJECT_PT_disabled(bpy.types.Panel):
    bl_label = "Disabled"
    bl_idname = "OBJECT_PT_disabled"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj is None:
            return

        if "disabled" in obj:
            layout.prop(obj, '["disabled"]', text="disabled")
        else:
            layout.operator("myaddon.add_disabled", text="Add Disabled")
