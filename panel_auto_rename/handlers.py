"""Handlers cho Auto Rename"""

import os

import bpy
from bpy.app.handlers import persistent

from . import utils


@persistent
def on_file_load_handler(_):
    success, message = utils.load_idp_data_from_json()
    if success:
        print(f"[SKLUM Auto Rename] {message}")

    context = bpy.context
    scene = getattr(context, "scene", None)
    if scene is None or not hasattr(scene, "sklum_auto_rename_settings"):
        return

    settings = scene.sklum_auto_rename_settings

    addon_name = __package__.split('.')[0]
    try:
        prefs = context.preferences.addons[addon_name].preferences
    except (KeyError, AttributeError, RuntimeError):
        prefs = None

    csv_path = prefs.csv_filepath if prefs else ""

    if csv_path and os.path.exists(bpy.path.abspath(csv_path)):
        settings.csv_filepath = csv_path
    elif not success:
        utils.clear_idp_cache()
        utils.set_last_loaded_csv(None)
        settings.csv_filepath = ""


def register():
    if on_file_load_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(on_file_load_handler)
    on_file_load_handler(None)


def unregister():
    if on_file_load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_file_load_handler)
