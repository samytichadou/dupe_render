import bpy


### REGISTER ---

def register():
    bpy.types.Scene.duperender_custom_frame_start = \
        bpy.props.IntProperty(name='Frame Start', default = 1)
    bpy.types.Scene.duperender_custom_frame_end = \
        bpy.props.IntProperty(name='Frame End', default = 250)
    bpy.types.Scene.duperender_previous_hash = \
        bpy.props.StringProperty() 

def unregister():
    del bpy.types.Scene.duperender_custom_frame_start
    del bpy.types.Scene.duperender_custom_frame_end
    del bpy.types.Scene.duperender_previous_hash