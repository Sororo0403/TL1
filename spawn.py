import os

import bpy


class SpawnNames:
    PROTOTYPE = 0
    INSTANCE = 1
    FILENAME = 2

    names = {
        "Enemy": ("PrototypeEnemySpawn", "EnemySpawn", "needle/needle.obj"),
        "Player": ("PrototypePlayerSpawn", "PlayerSpawn", "player/player.obj"),
    }


def get_available_obj_importers():
    importers = []

    if hasattr(bpy.ops.wm, "obj_import"):
        importers.append(bpy.ops.wm.obj_import)

    if hasattr(bpy.ops, "import_scene") and hasattr(bpy.ops.import_scene, "obj"):
        importers.append(bpy.ops.import_scene.obj)

    return importers


class MYADDON_OT_spawn_import_symbol(bpy.types.Operator):
    bl_idname = "myaddon.spawn_import_symbol"
    bl_label = "出現ポイントシンボル読み込み"
    bl_description = "出現ポイントのシンボルを読み込みます"
    bl_options = {"REGISTER", "UNDO"}

    def load_obj(self, type_name):
        if type_name not in SpawnNames.names:
            self.report({"WARNING"}, f"未定義の出現ポイント種別です: {type_name}")
            return {"CANCELLED"}

        spawn_data = SpawnNames.names[type_name]
        prototype_name = spawn_data[SpawnNames.PROTOTYPE]

        if bpy.data.objects.get(prototype_name) is not None:
            return {"FINISHED"}

        filepath = os.path.join(os.path.dirname(__file__), spawn_data[SpawnNames.FILENAME])
        if not os.path.isfile(filepath):
            self.report({"WARNING"}, f"モデルファイルが見つかりません: {filepath}")
            return {"CANCELLED"}

        before_names = set(bpy.data.objects.keys())
        bpy.ops.object.select_all(action="DESELECT")

        importers = get_available_obj_importers()
        if not importers:
            self.report({"WARNING"}, "利用可能なOBJインポート機能がありません")
            return {"CANCELLED"}

        errors = []
        for import_obj in importers:
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
            return {"CANCELLED"}

        imported_objects = [
            obj for obj in bpy.context.selected_objects if obj.name not in before_names
        ]
        if not imported_objects:
            imported_objects = [
                obj for obj in bpy.data.objects if obj.name not in before_names
            ]

        if not imported_objects:
            self.report({"WARNING"}, f"モデルを読み込めませんでした: {filepath}")
            return {"CANCELLED"}

        spawn_object = imported_objects[0]
        spawn_object.name = prototype_name
        if spawn_object.data is not None:
            spawn_object.data.name = prototype_name

        # プロトタイプは複製元としてだけ使うため、シーンには配置しない。
        for obj in imported_objects:
            for collection in list(obj.users_collection):
                collection.objects.unlink(obj)

        return {"FINISHED"}

    def execute(self, context):
        result = {"FINISHED"}

        for type_name in SpawnNames.names:
            if self.load_obj(type_name) == {"CANCELLED"}:
                result = {"CANCELLED"}

        return result
