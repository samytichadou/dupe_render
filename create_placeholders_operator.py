import bpy

from .handler import create_placeholders


class DUPERENDER_OT_create_placeholders(bpy.types.Operator):
    bl_idname = "duperender.create_placeholders"
    bl_label = "Create placeholders"
    bl_description = "Create empty files for detected Dupe frames"
    #bl_options = {'INTERNAL'}

    scene_range : bpy.props.BoolProperty(
        name = "Scene Frame Range",
        description="Remove placeholders in the scene frame range",
        default=True,
        )

    @classmethod
    def poll(cls, context):
        return context.scene.duperender_dupelist!=""

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "scene_range")

        box=layout.box()
        col=box.column(align=True)
        col.label(text="Proceed with caution", icon="ERROR")
        col.label(text="This action will create placeholders")
        col.label(text="Are you sure ?")  

    def execute(self, context):
        scn = context.scene
        create_placeholders(scn, self.scene_range)

        self.report({'INFO'}, "Placeholders created")
        
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_OT_create_placeholders)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_OT_create_placeholders)