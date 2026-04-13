import bpy

# ブレンダーに登録するアドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Taro Kamata",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "トップバー",
    "description": "トップバーにマニュアル項目を追加するレベルエディタ",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object",
}


# マニュアルを開くオペレータ
class WM_OT_open_manual(bpy.types.Operator):
    bl_idname = "wm.open_level_editor_manual"
    bl_label = "レベルエディタのマニュアルを開く"
    bl_description = "レベルエディタのマニュアルページをブラウザで開きます"

    def execute(self, context):
        bpy.ops.wm.url_open(url="https://www.blender.org/manual/")
        return {"FINISHED"}


# トップバーにメニュー項目を描画する関数
def draw_menu_manual(self, context):
    self.layout.operator(WM_OT_open_manual.bl_idname, text="マニュアル", icon="HELP")


# アドオン有効化時コールバック
def register():
    bpy.utils.register_class(WM_OT_open_manual)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_menu_manual)
    print("レベルエディタが有効化されました。")


# アドオン無効化時コールバック
def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_menu_manual)
    bpy.utils.unregister_class(WM_OT_open_manual)
    print("レベルエディタが無効化されました。")


if __name__ == "__main__":
    register()
