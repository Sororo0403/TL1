import json
import math
import os

import bpy
import bpy_extras
from mathutils import Vector

from .spawn import SpawnNames


class MYADDON_OT_import_scene(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "myaddon.import_scene"
    bl_label = "シーン読み込み"
    bl_description = "JSONからシーンを作成します"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={"HIDDEN"})
    clear_existing: bpy.props.BoolProperty(
        name="既存シーンを削除",
        description="読み込み前に現在のシーン内のオブジェクトを削除します",
        default=True,
    )

    def clear_scene(self):
        for obj in list(bpy.context.scene.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

    def import_obj(self, filepath):
        if not os.path.isfile(filepath):
            self.report({"WARNING"}, f"モデルファイルが見つかりません: {filepath}")
            return None

        before_names = set(bpy.data.objects.keys())
        bpy.ops.object.select_all(action="DESELECT")

        errors = []
        for import_obj in (bpy.ops.wm.obj_import, bpy.ops.import_scene.obj):
            try:
                import_obj(filepath=filepath)
                break
            except Exception as exc:
                errors.append(str(exc))
        else:
            self.report(
                {"WARNING"},
                f"モデルの読み込みに失敗しました: {filepath} ({'; '.join(errors)})",
            )
            return None

        imported_objects = [
            obj for obj in bpy.context.selected_objects if obj.name not in before_names
        ]
        if not imported_objects:
            imported_objects = [
                obj for obj in bpy.data.objects if obj.name not in before_names
            ]

        if not imported_objects:
            self.report({"WARNING"}, f"モデルを読み込めませんでした: {filepath}")
            return None

        root_obj = imported_objects[0]
        for child in imported_objects[1:]:
            child.parent = root_obj

        return root_obj

    def create_spawn_object(self, type_name):
        for spawn_type, spawn_data in SpawnNames.names.items():
            instance_name = spawn_data[SpawnNames.INSTANCE]
            prototype_name = spawn_data[SpawnNames.PROTOTYPE]
            if type_name != instance_name:
                continue

            prototype = bpy.data.objects.get(prototype_name)
            if prototype is None:
                bpy.ops.myaddon.spawn_import_symbol("EXEC_DEFAULT")
                prototype = bpy.data.objects.get(prototype_name)

            if prototype is None:
                self.report({"WARNING"}, f"プロトタイプが見つかりません: {prototype_name}")
                return None

            obj = prototype.copy()
            obj.data = prototype.data
            obj.name = instance_name
            obj["type"] = instance_name
            bpy.context.collection.objects.link(obj)
            return obj

        return None

    def create_empty_object(self, name):
        obj = bpy.data.objects.new(name, None)
        obj.empty_display_type = "CUBE"
        obj.empty_display_size = 1.0
        bpy.context.collection.objects.link(obj)
        return obj

    def create_object(self, data, base_dir):
        type_name = data.get("type", "EMPTY")

        obj = self.create_spawn_object(type_name)
        if obj is not None:
            return obj

        file_name = data.get("file_name")
        if file_name:
            filepath = file_name
            if not os.path.isabs(filepath):
                filepath = os.path.join(base_dir, filepath)
            obj = self.import_obj(filepath)
            if obj is not None:
                return obj

        name = data.get("name", type_name)
        return self.create_empty_object(name)

    def apply_object_data(self, obj, data, parent):
        obj.name = data.get("name", obj.name)

        if "type" in data:
            obj["type"] = data["type"]

        if "file_name" in data:
            obj["file_name"] = data["file_name"]

        collider = data.get("collider")
        if collider:
            obj["collider"] = collider.get("type", "BOX")
            obj["collider_center"] = Vector(collider.get("center", (0, 0, 0)))
            obj["collider_size"] = Vector(collider.get("size", (2, 2, 2)))

        if "disabled" in data:
            obj["disabled"] = data["disabled"]

        for key, value in data.get("custom_properties", {}).items():
            obj[key] = value

        obj.parent = parent

        transform = data.get("transform", {})
        translation = transform.get("translation", (0, 0, 0))
        rotation = transform.get("rotation", (0, 0, 0))
        scaling = transform.get("scaling", (1, 1, 1))

        obj.location = translation
        obj.rotation_euler = [math.radians(value) for value in rotation]
        obj.scale = scaling

    def import_object_tree(self, data, base_dir, parent=None):
        obj = self.create_object(data, base_dir)
        self.apply_object_data(obj, data, parent)

        for child_data in data.get("children", []):
            self.import_object_tree(child_data, base_dir, obj)

        return obj

    def execute(self, context):
        with open(self.filepath, "r", encoding="utf-8") as f:
            root = json.load(f)

        if self.clear_existing:
            self.clear_scene()

        base_dir = os.path.dirname(self.filepath)
        for obj_data in root.get("objects", []):
            self.import_object_tree(obj_data, base_dir)

        return {"FINISHED"}
