import bpy
import shutil
import os

from bpy.app.handlers import persistent

def create_placeholders(scene):
    dupe_list = scene.duperender_dupelist.split(",")
    base_dir = os.path.dirname(scene.render.frame_path(frame=1))
    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)
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
    or not scene.duperender_render\
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
    or not scene.duperender_render\
    or scene.duperender_dupelist == "":
        print("Dupe Render --- no Dupe Render operations (movie output/overwrite render used/no dupe/not scheduled)")
        return

    replace_placeholders(scene)


### REGISTER ---

def register():
    bpy.app.handlers.render_init.append(render_init_handler)
    bpy.app.handlers.render_complete.append(render_complete_handler)
    bpy.app.handlers.render_cancel.append(render_complete_handler)

def unregister():
    bpy.app.handlers.render_init.remove(render_init_handler)
    bpy.app.handlers.render_complete.remove(render_complete_handler)
    bpy.app.handlers.render_cancel.remove(render_complete_handler)