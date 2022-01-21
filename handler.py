import bpy
import shutil
import os

from bpy.app.handlers import persistent
from .hash_operator import get_frames_to_render

@persistent
def render_frame_handler(scene):
    current = scene.frame_current
    print("Dupe Render --- checking frame %i" % current)

    #check if frame in original list
    if not str(current) in scene.duperender_to_render_list.split(","):
        #copy file
        # print("Dupe Render --- copying dupe frame : %i" % current)
        # old_path = 
        # new_path = 
        # if not os.path.isfile(new_path):
        #     shutil.copy(old_path, new_path)
        pass
    else:
        print("Dupe Render --- original frame to render : %i" % current)

@persistent
def render_init_handler(scene):
    #check for overwrite off and dupe on
    #cleaning
    print("Dupe Render --- cleaning previous list")
    scene.duperender_to_render_list = ""
    #building list
    print("Dupe Render --- building list")
    fr_in = scene.frame_start
    fr_out = scene.frame_end
    dupe_list = get_frames_to_render(fr_in, fr_out, scene)[1]
    #scene.duperender_to_render_list = ",".join(str(e) for e in original_list)
    #creating empty files
    print("Dupe Render --- creating placeholder")


### REGISTER ---

def register():
    bpy.app.handlers.render_init.append(render_init_handler)
    #bpy.app.handlers.render_pre.append(render_frame_handler)

def unregister():
    bpy.app.handlers.render_init.remove(render_init_handler)
    #bpy.app.handlers.render_pre.remove(render_frame_handler)