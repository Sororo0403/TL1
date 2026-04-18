bl_info = {
    "name": "レベルエディタ",
    "author": "Taro Hatanaka",
    "version": (2, 0),
    "blender": (3, 3, 0),
    "category": "Object",
}

import bpy

from .draw_collider import DrawCollider
from .add_filename import MYADDON_OT_add_filename
from .add_collider import MYADDON_OT_add_collider
from .file_name import OBJECT_PT_file_name
from .collider import OBJECT_PT_collider
from .export_scene import MYADDON_OT_export_scene


class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu"

    def draw(self, context):
        self.layout.operator("myaddon.export_scene")


def submenu(self, context):
    self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


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


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(submenu)

    if DrawCollider.handle:
        bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle, "WINDOW")

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
