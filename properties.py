import bpy

class DUPERENDER_PR_framerange(bpy.types.PropertyGroup):
    frame_start : bpy.props.IntProperty(
        name = "Range Start Frame",
        default=1,
        )
    frame_end : bpy.props.IntProperty(
        name = "Range End Frame",
        default=250,
        )
    type : bpy.props.StringProperty(
        name = "Range Type",
        )

class DUPERENDER_PR_properties(bpy.types.PropertyGroup):
    dupelist : bpy.props.StringProperty(name="Dupe List")
    originallist : bpy.props.StringProperty(name="Original List") 
    use_duperender : bpy.props.BoolProperty(name="Use Dupe Render", default=True)
    render : bpy.props.BoolProperty(name="Use Dupe Render in animation render")
    frame_start : bpy.props.IntProperty(default=-1)
    frame_end : bpy.props.IntProperty(default=-1)
    processing_date : bpy.props.StringProperty()
    nb_fr_to_render : bpy.props.IntProperty(default=-1)
    nb_dupes_fr : bpy.props.IntProperty(default=-1)
    nb_fr_total : bpy.props.IntProperty(default=-1)
    gain : bpy.props.IntProperty(default=-1)
    is_processed : bpy.props.BoolProperty()

    specific_ranges : bpy.props.CollectionProperty(
        type = DUPERENDER_PR_framerange,
        name = "Specific Frame Ranges",
        )

### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_PR_framerange)
    bpy.utils.register_class(DUPERENDER_PR_properties)
    bpy.types.Scene.duperender_properties = \
        bpy.props.PointerProperty(type = DUPERENDER_PR_properties, name="Dupe Render Properties")

def unregister():
    bpy.utils.unregister_class(DUPERENDER_PR_framerange)
    bpy.utils.unregister_class(DUPERENDER_PR_properties)
    del bpy.types.Scene.duperender_properties
