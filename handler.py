import bpy
import shutil

from bpy.app.handlers import persistent

@persistent
def render_frame_handler(scene):
    current = scene.frame_current
    print("Dupe Render --- checking frame %i" % current)

    #check if frame in original list
    if not current in scene.duperender_to_render_list.split(","):
        #copy file
        pass

@persistent
def render_init_handler(scene):
    #cleaning
    print("Dupe Render --- cleaning memory")
    scene.duperender_to_render_list = ""
    #building list
        

### REGISTER ---

def register():
    bpy.app.handlers.render_init.append(render_init_handler)
    bpy.app.handlers.render_pre.append(render_frame_handler)

def unregister():
    bpy.app.handlers.render_init.remove(render_init_handler)
    bpy.app.handlers.render_pre.remove(render_frame_handler)