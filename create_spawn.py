import bpy

from .spawn import SpawnNames


class MYADDON_OT_spawn_create_symbol(bpy.types.Operator):
    bl_idname = "myaddon.spawn_create_symbol"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "出現ポイントのシンボルを作成します"
    bl_options = {"REGISTER", "UNDO"}

    type: bpy.props.StringProperty(name="Type", default="Player")

    def execute(self, context):
        if self.type not in SpawnNames.names:
            self.report({"WARNING"}, f"未定義の出現ポイント種別です: {self.type}")
            return {"CANCELLED"}

        spawn_data = SpawnNames.names[self.type]
        prototype_name = spawn_data[SpawnNames.PROTOTYPE]
        instance_name = spawn_data[SpawnNames.INSTANCE]

        prototype = bpy.data.objects.get(prototype_name)
        if prototype is None:
            bpy.ops.myaddon.spawn_import_symbol("EXEC_DEFAULT")
            prototype = bpy.data.objects.get(prototype_name)

        if prototype is None:
            self.report({"WARNING"}, f"プロトタイプが見つかりません: {prototype_name}")
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
        return bpy.ops.myaddon.spawn_create_symbol("EXEC_DEFAULT", type="Player")


class MYADDON_OT_spawn_create_enemy_symbol(bpy.types.Operator):
    bl_idname = "myaddon.spawn_create_enemy_symbol"
    bl_label = "敵出現ポイントシンボルの作成"
    bl_description = "敵出現ポイントのシンボルを作成します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return bpy.ops.myaddon.spawn_create_symbol("EXEC_DEFAULT", type="Enemy")
