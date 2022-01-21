import bpy
import shutil
import os

from bpy.app.handlers import persistent
#from .hash_operator import get_frames_to_render

# @persistent
# def render_init_handler(scene):
#     #check for overwrite off and animation render
#     if scene.render.use_overwrite:
#         print("Dupe Render --- render overwrite ON, no Dupe Render operations")
#         return

#     #cleaning
#     print("Dupe Render --- cleaning previous list")
#     scene.duperender_dupelist = ""

#     #building list
#     print("Dupe Render --- building list")
#     dupe_list = get_frames_to_render(scene.frame_start, scene.frame_end, scene)[1]
#     scene.duperender_dupelist = ",".join(str(e) for e in dupe_list)

#     #creating empty files
#     print("Dupe Render --- creating placeholders")
#     for f in dupe_list:
#         path = scene.render.frame_path(frame=f)
#         open(path, 'a').close()

def create_placeholders(scene):
    dupe_list = scene.duperender_dupelist.split(",")
    for dupe in dupe_list:
        f = int(dupe)
        path = scene.render.frame_path(frame=f)
        print("Dupe Render --- creating placeholder : %s" % path)
        open(path, 'a').close()

@persistent
def render_init_handler(scene):
    #check if dupe is used
    if scene.render.is_movie_format\
    or scene.render.use_overwrite\
    or not scene.duperender_next_render\
    or scene.duperender_dupelist == "":
        print("Dupe Render --- no Dupe Render operations (movie output/overwrite render used/no dupe/not scheduled)")
        return
    
    #creating empty files
    create_placeholders(scene)

def replace_placeholders(scene):
    dupe_list = scene.duperender_dupelist.split(",")

    for dupe in dupe_list:
        i = int(dupe)
        path = scene.render.frame_path(frame=i)
        if os.path.isfile(path):
            try:
                os.remove(path)
            except OSError as error:
                print(error)
                print("Dupe Render --- unable to duplicate frame %i, skipping" % i)
                continue
        chk_copy = False
        for f in range(i-1,scene.frame_start-1, -1):
            if str(f) not in dupe_list:
                oldpath = scene.render.frame_path(frame=f)
                print("Dupe Render --- duplicating frame %i to %s" % (f, path))
                if not os.path.isfile(oldpath):
                    break
                shutil.copy(oldpath, path)
                chk_copy = True
                break
        if not chk_copy:
            print("Dupe Render --- failed to find original frame for dupe : %i" % i)

@persistent
def render_complete_handler(scene):
    #check if dupe is used
    if scene.render.is_movie_format\
    or scene.render.use_overwrite\
    or not scene.duperender_next_render\
    or scene.duperender_dupelist == "":
        print("Dupe Render --- no Dupe Render operations (movie output/overwrite render used/no dupe/not scheduled)")
        return

    replace_placeholders(scene)

    #cleaning
    #scene.duperender_dupelist = ""
    scene.duperender_next_render = False

### REGISTER ---

def register():
    bpy.app.handlers.render_init.append(render_init_handler)
    bpy.app.handlers.render_complete.append(render_complete_handler)
    bpy.app.handlers.render_cancel.append(render_complete_handler)

def unregister():
    bpy.app.handlers.render_init.remove(render_init_handler)
    bpy.app.handlers.render_complete.remove(render_complete_handler)
    bpy.app.handlers.render_cancel.append(render_complete_handler)