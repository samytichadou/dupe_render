import bpy
import hashlib
import json
import time
from datetime import datetime

prop_exclude = [
    "frame_current",
    "frame_current_final",
    "frame_float",
]

### MATRIX
def world_matrix_to_hash(ob, dg) :
    mat = ob.evaluated_get(dg).matrix_world
    txt = ""
    for col in mat :
        for v in col : txt += str(v)
        
    return(hashlib.md5(txt.encode("utf-8")).hexdigest())
    
def get_matrix_hash(ob, dg) :
    lst = []
    lst.append(world_matrix_to_hash(ob,dg))

    if ob.type == "ARMATURE" :
        for bone in ob.pose.bones :
            lst.append(bone.name)
            for m in bone.matrix :
                for f in m : lst.append(str(f))

    hash = hashlib.md5(str(lst).encode("utf-8")).hexdigest()

    return hash
    
def get_scene_objects_matrix_hash() :
    dg = bpy.context.evaluated_depsgraph_get()
    
    lst = []
    for ob in bpy.context.scene.objects:
        lst.append(get_matrix_hash(ob, dg))
   
    return hashlib.md5(str(lst).encode("utf-8")).hexdigest()

### PROPS
def is_serializable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False

def get_props_hash(ob):
    lst = []
    for p in ob.bl_rna.properties:
        if p.identifier not in prop_exclude:
            lst.append(p.identifier + str(getattr(ob, p.identifier)))
        # else:
        #     print("prop avoided --- %s" % p.identifier)
    try:
        for p in ob.data.bl_rna.properties:
            if p.identifier not in prop_exclude:
                lst.append(p.identifier + str(getattr(ob.data, p.identifier)))
            # else:
            #     print("prop avoided --- %s" % p.identifier)
    except AttributeError:
        pass
    return hashlib.md5(str(lst).encode("utf-8")).hexdigest()

def get_nodetree_hash(nodetree):
    lst = []
    for n in nodetree.nodes:
        lst.append(get_props_hash(n))
        for i in n.inputs:
            lst.append(i.identifier)
            try:
                if i.type=="VALUE":
                    lst.append(str(i.default_value))
                else:
                    for n in range(len(i.default_value)):
                        lst.append(str(i.default_value[n]))
            except AttributeError:
                pass
    return hashlib.md5(str(lst).encode("utf-8")).hexdigest()

def get_shader_hash(ob):
    lst = []
    for s in ob.material_slots:
        lst.append(get_nodetree_hash(s.material.node_tree))
    return hashlib.md5(str(lst).encode("utf-8")).hexdigest()

def get_materials_hash():
    lst = []
    for m in bpy.data.materials:
        if (m.users > 0 and not m.use_fake_user)\
        or (m.use_fake_user and m.users > 1):
            lst.append(get_props_hash(m))
            if m.node_tree:
                lst.append(get_nodetree_hash(m.node_tree))
    return hashlib.md5(str(lst).encode("utf-8")).hexdigest()

def get_modifiers_hash():
    lst = []
    for ob in bpy.context.scene.objects:
        if not ob.hide_render:
            for m in ob.modifiers:
                lst.append(get_props_hash(m))
    return hashlib.md5(str(lst).encode("utf-8")).hexdigest()

def get_custom_props_hash(ob):
    lst = []
    for k in ob.keys():
        lst.append(k)
        lst.append(getattr(ob, '["%s"]' % k))
    return hashlib.md5(str(lst).encode("utf-8")).hexdigest()  

def get_objects_props_hash():
    lst = []
    for ob in bpy.context.scene.objects:
        if not ob.hide_render:
            lst.append(get_props_hash(ob))
            if ob.data:
                lst.append(get_props_hash(ob.data))
            lst.append(get_custom_props_hash(ob))
            #lst.append(get_shader_hash(ob))
    return hashlib.md5(str(lst).encode("utf-8")).hexdigest()

def get_scene_props_hash():
    scn = bpy.context.scene
    lst = []

    # scene props
    lst.append(get_props_hash(scn))
    # world props
    lst.append(get_props_hash(scn.world))
    # objects props
    for ob in scn.objects:
        lst.append(get_props_hash(ob))
        
    hash = hashlib.md5(str(lst).encode("utf-8")).hexdigest()
    
    return hash

### FINAL HASH
def get_frame_hash():
    lst = []
    lst.append(get_scene_objects_matrix_hash())
    lst.append(get_scene_props_hash())
    lst.append(get_modifiers_hash())
    lst.append(get_objects_props_hash())
    lst.append(get_materials_hash())

    hash = hashlib.md5(str(lst).encode("utf-8")).hexdigest()
    return hash

def get_frames_to_render(context):
    scn = context.scene

    #update cursor
    wm = context.window_manager
    upd_value = 1000/(scn.frame_end-scn.frame_start+1)
    wm.progress_begin(0, 1000)

    hash_list = []
    frame_list = []
    dupe_list = []
    old_frame = scn.frame_current

    i=0
    n=0
    for f in range(scn.frame_start, scn.frame_end + 1):
        i+=upd_value
        wm.progress_update(int(i))
        scn.frame_current = f
        hash = get_frame_hash()
        print("Dupe Render --- frame %i : %s" % (f, hash))
        # if hash not in hash_list:
        if not hash_list or hash!=hash_list[n-1]:
            hash_list.append(hash)
            n+=1
            frame_list.append(f)
        else:
            dupe_list.append(f)

    wm.progress_end()
    scn.frame_current = old_frame
    return frame_list, dupe_list


class DUPERENDER_OT_find_dupe_frames(bpy.types.Operator):
    bl_idname = "duperender.find_dupe_frames"
    bl_label = "Process dupe frames"
    bl_description = "Process dupe images to skip on next render"
    #bl_options = {'INTERNAL'}

    original_frames_string : bpy.props.StringProperty(
        name = "Original Frames List",
        description="Frames to Render, you can copy paste this list",
        )
    total_frames = 0
    original_frames_nb = 0
    dupe_frames = 0
    range_error = False
    final_range = ""
    dupe_frames_string = ""
    process_time = ""
    render_gain = 0

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        scn = context.scene

        fr_in = scn.frame_start
        fr_out = scn.frame_end

        start_time = time.time()
        original_list, dupe_list = get_frames_to_render(context)
        self.process_time = str(time.time() - start_time)

        self.final_range = "%i - %i" % (fr_in, fr_out)
        self.original_frames_nb = len(original_list)
        self.total_frames = fr_out - fr_in + 1
        self.dupe_frames = self.total_frames - self.original_frames_nb
        self.original_frames_string = ",".join(str(e) for e in original_list)
        self.dupe_frames_string = ",".join(str(e) for e in dupe_list)
        self.render_gain = int((self.total_frames-self.original_frames_nb)/(self.total_frames/100))

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout

        layout.label(text="Range : %s" % self.final_range)
        layout.label(text="Processed in %s seconds" % self.process_time)
        col = layout.column(align=True)
        col.label(text="%i frame(s) to render out of %i" % (self.original_frames_nb, self.total_frames))
        col.prop(self, "original_frames_string", text="")
        col.separator()
        col.label(text="%i dupe(s) could be skipped" % self.dupe_frames)
        col.label(text="%i%% render gain" % self.render_gain)
        layout.label(text="OK to set dupe render")       

    def execute(self, context):
        scn = context.scene
        props = scn.duperender_properties

        props.dupelist = self.dupe_frames_string
        props.originallist = self.original_frames_string
        props.render = True

        props.frame_start = scn.frame_start
        props.frame_end = scn.frame_end

        props.nb_fr_to_render = self.original_frames_nb
        props.nb_dupes_fr = self.dupe_frames
        props.nb_fr_total = self.total_frames

        props.gain = self.render_gain

        props.processing_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        props.is_processed = True

        # redraw props gui
        for area in context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "Dupe Frames set")
        
        return {'FINISHED'}


class DUPERENDER_OT_hash_frame(bpy.types.Operator):
    bl_idname = "duperender.hash_frame"
    bl_label = "Hash Frame"
    bl_description = ""
    #bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        hash = get_frame_hash()
        self.report({'INFO'}, "Current frame hash --- %s" % hash)
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_OT_find_dupe_frames)
    bpy.utils.register_class(DUPERENDER_OT_hash_frame)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_OT_find_dupe_frames)
    bpy.utils.unregister_class(DUPERENDER_OT_hash_frame)