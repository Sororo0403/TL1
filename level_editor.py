import bpy
import math
import json
import bpy_extras

# =========================
# アドオン情報
# =========================
bl_info = {
    "name": "レベルエディタ",
    "author": "Taro Kamata",
    "version": (1, 4),
    "blender": (3, 3, 1),
    "location": "トップバー",
    "description": "レベルエディタ",
    "category": "Object",
}


# =========================
# カスタムプロパティ追加Operator
# =========================
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.add_filename"
    bl_label = "FileName追加"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.object["file_name"] = ""
        return {"FINISHED"}


# =========================
# Panel（UI）
# =========================
class OBJECT_PT_file_name(bpy.types.Panel):
    bl_idname = "OBJECT_PT_file_name"
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj is None:
            return

        # すでにある場合
        if "file_name" in obj:
            layout.prop(obj, '["file_name"]', text="FileName")
        else:
            layout.operator("myaddon.add_filename")


# =========================
# シーン出力
# =========================
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.export_scene"
    bl_label = "シーン出力（JSON）"

    filename_ext = ".json"

    def execute(self, context):

        print("==== シーン出力開始 ====")

        objects = list(context.scene.objects)

        # ID割り当て
        id_map = {obj: i for i, obj in enumerate(objects)}

        data = []

        for obj in objects:

            loc, rot, scale = obj.matrix_local.decompose()

            rot_euler = rot.to_euler()
            rot_deg = (
                math.degrees(rot_euler.x),
                math.degrees(rot_euler.y),
                math.degrees(rot_euler.z),
            )

            obj_id = id_map[obj]
            parent_id = id_map[obj.parent] if obj.parent else -1

            entry = {
                "id": obj_id,
                "name": obj.name,
                "type": obj.type,
                "position": [loc.x, loc.y, loc.z],
                "rotation": list(rot_deg),
                "scale": [scale.x, scale.y, scale.z],
                "parent": parent_id,
            }

            # 🔥 カスタムプロパティ追加
            if "file_name" in obj:
                entry["file_name"] = obj["file_name"]

            data.append(entry)

        path = self.filepath

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("保存成功:", path)
            self.report({"INFO"}, "シーン出力成功")

        except Exception as e:
            print("保存失敗:", e)
            self.report({"ERROR"}, "保存失敗")

        return {"FINISHED"}


# =========================
# メニュー
# =========================
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu"

    def draw(self, context):
        layout = self.layout
        layout.operator("myaddon.export_scene", icon="EXPORT")


# =========================
# トップバー追加
# =========================
def submenu(self, context):
    self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


# =========================
# 登録
# =========================
classes = (
    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.append(submenu)
    print("レベルエディタが有効化されました。")


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(submenu)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print("レベルエディタが無効化されました。")


if __name__ == "__main__":
    register()
