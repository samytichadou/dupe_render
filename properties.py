import bpy


### REGISTER ---

def register():
    bpy.types.Scene.duperender_dupelist = \
        bpy.props.StringProperty(name="Dupe List")
    bpy.types.Scene.duperender_originallist = \
        bpy.props.StringProperty(name="Original List") 
    bpy.types.Scene.duperender_use_duperender = \
        bpy.props.BoolProperty(name="Use Dupe Render", default=True)
    bpy.types.Scene.duperender_render = \
        bpy.props.BoolProperty(name="Use Dupe Render in animation render")
    bpy.types.Scene.duperender_frame_start = \
        bpy.props.IntProperty(default=-1)
    bpy.types.Scene.duperender_frame_end = \
        bpy.props.IntProperty(default=-1)
    bpy.types.Scene.duperender_processing_date = \
        bpy.props.StringProperty()
    bpy.types.Scene.duperender_nb_fr_to_render = \
        bpy.props.IntProperty(default=-1)
    bpy.types.Scene.duperender_nb_fr_total = \
        bpy.props.IntProperty(default=-1)
    bpy.types.Scene.duperender_gain = \
        bpy.props.IntProperty(default=-1)

def unregister():
    del bpy.types.Scene.duperender_dupelist
    del bpy.types.Scene.duperender_originallist
    del bpy.types.Scene.duperender_use_duperender
    del bpy.types.Scene.duperender_render