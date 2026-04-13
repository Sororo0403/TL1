import bpy

# アドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Taro Kamata",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "トップバー",
    "description": "レベルエディタ",
    "category": "Object",
}


# =========================
# オペレータ①（頂点を伸ばす）
# =========================
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点を伸ばします"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.object

        if obj and obj.type == "MESH":
            for v in obj.data.vertices:
                v.co.x += 1.0

        print("頂点を伸ばしました")
        return {"FINISHED"}


# =========================
# オペレータ②（ICO球生成）
# =========================
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_ico_sphere"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")
        return {"FINISHED"}


# =========================
# サブメニュークラス
# =========================
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu"
    bl_description = "拡張メニュー by " + bl_info["author"]

    def draw(self, context):
        layout = self.layout

        # オペレータ追加
        layout.operator(MYADDON_OT_stretch_vertex.bl_idname)
        layout.operator(MYADDON_OT_create_ico_sphere.bl_idname)

        # マニュアル
        layout.operator("wm.url_open", text="マニュアル", icon="HELP").url = (
            "https://www.blender.org/manual/"
        )


# =========================
# トップバーに追加
# =========================
def submenu(self, context):
    self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


# =========================
# 登録クラス
# =========================
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    TOPBAR_MT_my_menu,
)


# =========================
# 有効化
# =========================
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.append(submenu)
    print("レベルエディタが有効化されました。")


# =========================
# 無効化
# =========================
def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(submenu)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print("レベルエディタが無効化されました。")


if __name__ == "__main__":
    register()
