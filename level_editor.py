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
# サブメニュークラス
# =========================
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu"
    bl_description = "拡張メニュー by " + bl_info["author"]

    def draw(self, context):
        layout = self.layout

        # サブメニューの中身
        layout.operator("wm.url_open", text="マニュアル", icon="HELP").url = (
            "https://www.blender.org/manual/"
        )


# =========================
# トップバーに追加する関数
# =========================
def submenu(self, context):
    self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


# =========================
# 登録するクラスリスト
# =========================
classes = (TOPBAR_MT_my_menu,)


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

    for cls in classes:
        bpy.utils.unregister_class(cls)

    print("レベルエディタが無効化されました。")


if __name__ == "__main__":
    register()
