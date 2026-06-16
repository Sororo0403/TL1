import bpy

from .spawn import SpawnNames


def create_spawn_symbol(operator, context, type_name):
    if type_name not in SpawnNames.names:
        operator.report({"WARNING"}, f"未定義の出現ポイント種別です: {type_name}")
        return {"CANCELLED"}

    spawn_data = SpawnNames.names[type_name]
    prototype_name = spawn_data[SpawnNames.PROTOTYPE]
    instance_name = spawn_data[SpawnNames.INSTANCE]

    prototype = bpy.data.objects.get(prototype_name)
    if prototype is None:
        bpy.ops.myaddon.spawn_import_symbol("EXEC_DEFAULT")
        prototype = bpy.data.objects.get(prototype_name)

    if prototype is None:
        operator.report({"WARNING"}, f"プロトタイプが見つかりません: {prototype_name}")
        return {"CANCELLED"}

    obj = prototype.copy()
    obj.data = prototype.data
    obj.name = instance_name
    obj["type"] = instance_name
    obj.location = context.scene.cursor.location

    context.collection.objects.link(obj)

    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    context.view_layer.objects.active = obj

    return {"FINISHED"}


class MYADDON_OT_spawn_create_player_symbol(bpy.types.Operator):
    bl_idname = "myaddon.spawn_create_player_symbol"
    bl_label = "プレイヤー出現ポイントシンボルの作成"
    bl_description = "プレイヤー出現ポイントのシンボルを作成します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return create_spawn_symbol(self, context, "Player")


class MYADDON_OT_spawn_create_enemy_symbol(bpy.types.Operator):
    bl_idname = "myaddon.spawn_create_enemy_symbol"
    bl_label = "敵出現ポイントシンボルの作成"
    bl_description = "敵出現ポイントのシンボルを作成します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return create_spawn_symbol(self, context, "Enemy")
