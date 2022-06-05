import bpy
import shutil
import os

from bpy.app.handlers import persistent

def create_placeholders(scene, scene_range=True):
    dupe_list = scene.duperender_dupelist.split(",")
    base_dir = os.path.dirname(scene.render.frame_path(frame=1))

    if scene_range:
        frame_range=range(scene.frame_start, scene.frame_end+1)
    else:
        frame_range=range(scene.duperender_frame_start, scene.duperender_frame_end+1)

    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)
    for dupe in dupe_list:
        f = int(dupe)
        if f in frame_range and f!=scene.frame_start:
            path = scene.render.frame_path(frame=f)
            if os.path.isfile(path):
                print("Dupe Render --- file already exists : %s" % path)
            else:
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
    
def search_original_from_dupe(frame, scene):
    dupe_list = scene.duperender_dupelist.split(",")
    for f in range(frame-1,scene.frame_start-1, -1):
        if str(f) not in dupe_list:
            return f
    if frame!=scene.frame_start:
        return scene.frame_start
    return None

def replace_placeholders(scene, scene_range=True):
    dupe_list = scene.duperender_dupelist.split(",")

    if scene_range:
        frame_range=range(scene.frame_start, scene.frame_end+1)
    else:
        frame_range=range(scene.duperender_frame_start, scene.duperender_frame_end+1)

    for dupe in dupe_list:
        i = int(dupe)
        if i in frame_range:
            path = scene.render.frame_path(frame=i)
            original = search_original_from_dupe(i, scene)
            if original is not None:
                #remove dupe frame
                if os.path.isfile(path):
                    #check if placeholder
                    if os.path.getsize(path)!=0:
                        print("Dupe Render --- frame %i is not a placeholder, skipping" % i)
                        continue
                    try:
                        os.remove(path)
                    except OSError as error:
                        print(error)
                        print("Dupe Render --- unable to remove frame %i, skipping" % i)
                        continue
                chk_copy = False
                oldpath = scene.render.frame_path(frame=original)
                if not os.path.isfile(oldpath):
                    print("Dupe Render --- failed to find original frame for dupe : %i" % i)
                    continue
                print("Dupe Render --- duplicating frame %i to %s" % (i, path))
                shutil.copy(oldpath, path)

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