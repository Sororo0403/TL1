import bpy
import json
import math
import bpy_extras


class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.export_scene"
    bl_label = "シーン出力"

    filename_ext = ".json"

    def parse_object(self, parent_list, obj):
        data = {}
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
                self.parse_object(data["children"], child)

    def execute(self, context):
        root = {"name": "scene", "objects": []}

        for obj in bpy.context.scene.objects:
            if obj.parent is None:
                self.parse_object(root["objects"], obj)

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(root, f, indent=4, ensure_ascii=False)

        return {"FINISHED"}
