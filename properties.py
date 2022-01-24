import bpy


### REGISTER ---

def register():
    bpy.types.Scene.duperender_dupelist = \
        bpy.props.StringProperty(name="Dupe List")
    bpy.types.Scene.duperender_originallist = \
        bpy.props.StringProperty(name="Original List") 
    bpy.types.Scene.duperender_use_duperender = \
        bpy.props.BoolProperty(name="Use Dupe Render", default=True)
    bpy.types.Scene.duperender_next_render = \
        bpy.props.BoolProperty(name="Use Dupe Render in Next Render")

def unregister():
    del bpy.types.Scene.duperender_dupelist
    del bpy.types.Scene.duperender_originallist
    del bpy.types.Scene.duperender_use_duperender
    del bpy.types.Scene.duperender_next_render