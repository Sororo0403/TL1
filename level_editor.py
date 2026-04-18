import bpy
import math
import json
import bpy_extras
import gpu
import gpu_extras.batch
from mathutils import Vector

# =========================
# アドオン情報
# =========================
bl_info = {
    "name": "レベルエディタ（JSONツリー版）",
    "author": "Taro Hatanaka",
    "version": (2, 0),
    "blender": (3, 3, 1),
    "location": "トップバー",
    "description": "レベルエディタ（JSONツリー構造対応）",
    "category": "Object",
}


# =========================
# コライダー描画
# =========================
class DrawCollider:
    handle = None

    @staticmethod
    def draw_collider():
        vertices = {"pos": []}
        indices = []

        offsets = [
            (-0.5, -0.5, -0.5),
            (0.5, -0.5, -0.5),
            (-0.5, 0.5, -0.5),
            (0.5, 0.5, -0.5),
            (-0.5, -0.5, 0.5),
            (0.5, -0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
        ]

        for obj in bpy.context.scene.objects:
            if "collider" not in obj:
                continue

            start = len(vertices["pos"])

            center = obj["collider_center"]
            size = obj["collider_size"]

            for offset in offsets:
                pos = Vector(center)

                pos.x += offset[0] * size[0]
                pos.y += offset[1] * size[1]
                pos.z += offset[2] * size[2]

                pos = obj.matrix_world @ pos
                vertices["pos"].append(pos)

            edges = [
                (0, 1),
                (2, 3),
                (0, 2),
                (1, 3),
                (4, 5),
                (6, 7),
                (4, 6),
                (5, 7),
                (0, 4),
                (1, 5),
                (2, 6),
                (3, 7),
            ]

            for e in edges:
                indices.append((start + e[0], start + e[1]))

        if not vertices["pos"]:
            return

        shader = gpu.shader.from_builtin("UNIFORM_COLOR")
        batch = gpu_extras.batch.batch_for_shader(
            shader, "LINES", vertices, indices=indices
        )

        shader.bind()
        shader.uniform_float("color", (0.2, 0.8, 1.0, 1.0))
        batch.draw(shader)


# =========================
# FileName追加
# =========================
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.add_filename"
    bl_label = "FileName追加"

    def execute(self, context):
        context.object["file_name"] = ""
        return {"FINISHED"}


# =========================
# Collider追加
# =========================
class MYADDON_OT_add_collider(bpy.types.Operator):
    bl_idname = "myaddon.add_collider"
    bl_label = "コライダー追加"

    def execute(self, context):
        obj = context.object
        obj["collider"] = "BOX"
        obj["collider_center"] = Vector((0.0, 0.0, 0.0))
        obj["collider_size"] = Vector((2.0, 2.0, 2.0))
        return {"FINISHED"}


# =========================
# FileNameパネル
# =========================
class OBJECT_PT_file_name(bpy.types.Panel):
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj is None:
            return

        if "file_name" in obj:
            layout.prop(obj, '["file_name"]')
        else:
            layout.operator("myaddon.add_filename")


# =========================
# Colliderパネル
# =========================
class OBJECT_PT_collider(bpy.types.Panel):
    bl_label = "Collider"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj is None:
            return

        if "collider" in obj:
            layout.prop(obj, '["collider"]')
            layout.prop(obj, '["collider_center"]')
            layout.prop(obj, '["collider_size"]')
        else:
            layout.operator("myaddon.add_collider")


# =========================
# JSONエクスポート
# =========================
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.export_scene"
    bl_label = "シーン出力（JSON）"

    filename_ext = ".json"

    # 再帰関数
    def parse_object(self, parent_list, obj):

        data = {}

        data["type"] = obj.type
        data["name"] = obj.name

        # Transform
        loc, rot, scale = obj.matrix_local.decompose()
        rot = rot.to_euler()

        data["transform"] = {
            "translation": [loc.x, loc.y, loc.z],
            "rotation": [
                math.degrees(rot.x),
                math.degrees(rot.y),
                math.degrees(rot.z),
            ],
            "scaling": [scale.x, scale.y, scale.z],
        }

        # file_name
        if "file_name" in obj:
            data["file_name"] = obj["file_name"]

        # collider
        if "collider" in obj:
            data["collider"] = {
                "type": obj["collider"],
                "center": list(obj["collider_center"]),
                "size": list(obj["collider_size"]),
            }

        parent_list.append(data)

        # 子供（再帰）
        if len(obj.children) > 0:
            data["children"] = []
            for child in obj.children:
                self.parse_object(data["children"], child)

    def execute(self, context):

        json_root = {}
        json_root["name"] = "scene"
        json_root["objects"] = []

        # ルートオブジェクトだけ
        for obj in bpy.context.scene.objects:
            if obj.parent is None:
                self.parse_object(json_root["objects"], obj)

        json_text = json.dumps(json_root, indent=4, ensure_ascii=False)

        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(json_text)

        self.report({"INFO"}, "JSON出力成功")
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


def submenu(self, context):
    self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


# =========================
# 登録
# =========================
classes = (
    MYADDON_OT_add_filename,
    MYADDON_OT_add_collider,
    OBJECT_PT_file_name,
    OBJECT_PT_collider,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.append(submenu)

    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(
        DrawCollider.draw_collider, (), "WINDOW", "POST_VIEW"
    )

    print("アドオン有効化")


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(submenu)

    if DrawCollider.handle:
        bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle, "WINDOW")

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print("アドオン無効化")


if __name__ == "__main__":
    register()
