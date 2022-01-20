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


class DUPERENDER_OT_preview_dupe_render(bpy.types.Operator):
    bl_idname = "duperender.preview_dupe_render"
    bl_label = "Preview Dupe Render"
    bl_description = ""
    #bl_options = {'INTERNAL'}

    custom_range : bpy.props.BoolProperty()
    original_frames_list : bpy.props.StringProperty(
        name = "Original Frames List",
        description="Frames to Render, you can copy paste this list",
        )
    total_frames = 0
    original_frames = 0
    dupe_frames = 0
    range_error = False
    final_range = ""

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        hash_list = []

        scn = context.scene
        old_frame = scn.frame_current
        original_frames = ""

        if not self.custom_range:
            fr_in = scn.frame_start
            fr_out = scn.frame_end
        else:
            fr_in = scn.duperender_custom_frame_start
            fr_out = scn.duperender_custom_frame_end
            if fr_in >= fr_out:
                self.range_error = True
                return context.window_manager.invoke_props_dialog(self)

        self.final_range = "%i - %i" % (fr_in, fr_out)

        for f in range(fr_in, fr_out + 1):
            scn.frame_current = f
            hash = get_frame_hash()
            print("frame %i --- %s" % (f, hash))
            if hash not in hash_list:
                hash_list.append(get_frame_hash())
                original_frames += "%i, " % f

        self.original_frames = len(hash_list)
        self.total_frames = fr_out - fr_in + 1
        self.dupe_frames = self.total_frames - self.original_frames
        self.original_frames_list = original_frames[:-2]

        scn.frame_current = old_frame

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout


        if not self.range_error:
            layout.label(text="Range : %s" % self.final_range)
            col = layout.column(align=True)
            col.label(text="%i frame(s) to render out of %i" % (self.original_frames, self.total_frames))
            col.prop(self, "original_frames_list", text="")
            col.separator()
            col.label(text="%i dupe(s) could be skipped" % self.dupe_frames)
        else:
            layout.label(text="Custom End Frame must be superior to Custom Start Frame")

    def execute(self, context):
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
    bpy.utils.register_class(DUPERENDER_OT_preview_dupe_render)
    bpy.utils.register_class(DUPERENDER_OT_hash_frame)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_OT_preview_dupe_render)
    bpy.utils.unregister_class(DUPERENDER_OT_hash_frame)