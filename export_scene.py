import bpy
import json
import math
import os
import bpy_extras
from pathlib import Path

WP0_LEVEL_PATH = Path(
    os.path.expanduser("~/source/repos/WP0/game/resources/levels/scene.json")
)

EXPORTED_PROPERTY_KEYS = {
    "_RNA_UI",
    "type",
    "file_name",
    "collider",
    "collider_center",
    "collider_size",
}


def to_json_value(value):
    if isinstance(value, (str, bool, int, float)) or value is None:
        return value

    if hasattr(value, "to_list"):
        return value.to_list()

    if hasattr(value, "__iter__"):
        return [to_json_value(item) for item in value]

    return str(value)


def parse_object(parent_list, obj):
    data = {}
    if "type" in obj:
        data["type"] = obj["type"]
    else:
        data["type"] = obj.type
    data["name"] = obj.name

    loc, rot, scale = obj.matrix_local.decompose()
    rot = rot.to_euler()

    data["transform"] = {
        "translation": [loc.x, loc.y, loc.z],
        "rotation": [math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z)],
        "scaling": [scale.x, scale.y, scale.z],
    }

    if "file_name" in obj:
        data["file_name"] = obj["file_name"]

    custom_properties = {}
    for key in obj.keys():
        if key in EXPORTED_PROPERTY_KEYS:
            continue
        custom_properties[key] = to_json_value(obj[key])

    if custom_properties:
        data["custom_properties"] = custom_properties

    if "collider" in obj:
        data["collider"] = {
            "type": obj["collider"],
            "center": list(obj["collider_center"]),
            "size": list(obj["collider_size"]),
        }

    parent_list.append(data)

    if obj.children:
        data["children"] = []
        for child in obj.children:
            parse_object(data["children"], child)


def build_scene_root():
    root = {"name": "scene", "objects": []}

    for obj in bpy.context.scene.objects:
        if obj.parent is None:
            parse_object(root["objects"], obj)

    return root


def write_scene(filepath):
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(build_scene_root(), f, indent=4, ensure_ascii=False)

    return output_path


class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.export_scene"
    bl_label = "シーン出力"

    filename_ext = ".json"

    def parse_object(self, parent_list, obj):
        parse_object(parent_list, obj)

    def execute(self, context):
        write_scene(self.filepath)
        return {"FINISHED"}


class MYADDON_OT_export_wp0_scene(bpy.types.Operator):
    bl_idname = "myaddon.export_wp0_scene"
    bl_label = "WP0へシーン出力"
    bl_description = "WP0/game/resources/levels/scene.json に出力します"

    def execute(self, context):
        output_path = write_scene(WP0_LEVEL_PATH)
        self.report({"INFO"}, f"WP0へ出力しました: {output_path}")
        return {"FINISHED"}
