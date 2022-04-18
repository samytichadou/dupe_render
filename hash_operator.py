import bpy
import hashlib
import json

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
        
    hash = hashlib.md5(str(lst).encode("utf-8")).hexdigest()
    
    return hash

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
    hash = hashlib.md5(str(lst).encode("utf-8")).hexdigest()
    return hash

def get_scene_props_hash() :
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

    hash = hashlib.md5(str(lst).encode("utf-8")).hexdigest()
    return hash

def get_frames_to_render(scn):
    hash_list = []
    frame_list = []
    dupe_list = []
    old_frame = scn.frame_current

    for f in range(scn.frame_start, scn.frame_end + 1):
        scn.frame_current = f
        hash = get_frame_hash()
        print("frame %i --- %s" % (f, hash))
        if hash not in hash_list:
            hash_list.append(hash)
            frame_list.append(f)
        else:
            dupe_list.append(f)

    scn.frame_current = old_frame
    return frame_list, dupe_list


class DUPERENDER_OT_find_dupe_frames(bpy.types.Operator):
    bl_idname = "duperender.find_dupe_frames"
    bl_label = "Find dupe frames"
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

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        scn = context.scene

        fr_in = scn.frame_start
        fr_out = scn.frame_end

        original_list, dupe_list = get_frames_to_render(scn)

        self.final_range = "%i - %i" % (fr_in, fr_out)
        self.original_frames_nb = len(original_list)
        self.total_frames = fr_out - fr_in + 1
        self.dupe_frames = self.total_frames - self.original_frames_nb
        self.original_frames_string = ",".join(str(e) for e in original_list)
        self.dupe_frames_string = ",".join(str(e) for e in dupe_list)

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout

        layout.label(text="Range : %s" % self.final_range)
        col = layout.column(align=True)
        col.label(text="%i frame(s) to render out of %i" % (self.original_frames_nb, self.total_frames))
        col.prop(self, "original_frames_string", text="")
        col.separator()
        col.label(text="%i dupe(s) could be skipped" % self.dupe_frames)
        layout.label(text="OK to schedule dupe frames for next render")       

    def execute(self, context):
        scn = context.scene
        scn.duperender_dupelist = self.dupe_frames_string
        scn.duperender_originallist = self.original_frames_string
        scn.duperender_render = True

        # redraw props gui
        for area in context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "Dupe Frames scheduled")
        
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