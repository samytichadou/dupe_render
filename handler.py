import bpy
import shutil

from bpy.app.handlers import persistent

from .hash_operator import get_frame_hash

@persistent
def render_init_handler(scene):

    print("Dupe Render --- checking frame")
    current_hash = get_frame_hash()

    if scene.duperender_previous_hash == current_hash:
        print("Dupe Render --- duped frame copying")

    print("Dupe Render --- writing hash in memory")
    scene.duperender_previous_hash = current_hash

@persistent
def render_write_handler(scene):
    print("writing handler")
    print(scene.frame_current)
    

### REGISTER ---

def register():
    bpy.app.handlers.render_init.append(render_init_handler)
    bpy.app.handlers.render_write.append(render_write_handler)

def unregister():
    bpy.app.handlers.render_init.remove(render_init_handler)
    bpy.app.handlers.render_write.remove(render_write_handler)