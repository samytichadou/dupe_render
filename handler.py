import bpy
import shutil
import datetime

from bpy.app.handlers import persistent

@persistent
def start_handler(scene):
    print("test_start_handler")

@persistent
def end_handler(scene):
    print("test_end_handler")

@persistent
def deps_handler_start(scene):
    print("deps_handler start - " + str(datetime.datetime.now()))

@persistent
def deps_handler_end(scene):
    print("deps_handler end - " + str(datetime.datetime.now()))


### REGISTER ---

def register():
    bpy.app.handlers.render_init.append(start_handler)
    bpy.app.handlers.render_write.append(end_handler)
    bpy.app.handlers.depsgraph_update_pre.append(deps_handler_start)
    bpy.app.handlers.depsgraph_update_post.append(deps_handler_start)

def unregister():
    bpy.app.handlers.render_init.remove(start_handler)
    bpy.app.handlers.render_write.remove(end_handler)
    bpy.app.handlers.depsgraph_update_pre.remove(deps_handler_start)
    bpy.app.handlers.depsgraph_update_post.remove(deps_handler_start)