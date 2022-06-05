import bpy

from .handler import create_placeholders


class DUPERENDER_OT_create_placeholders(bpy.types.Operator):
    bl_idname = "duperender.create_placeholders"
    bl_label = "Create placeholders"
    bl_description = "Create empty files for detected Dupe frames"
    #bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.scene.duperender_dupelist!=""

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        col=layout.column(align=True)
        col.label(text="Proceed with caution", icon="ERROR")
        col.label(text="This action will create placeholders")
        col.label(text="Are you sure ?")  

    def execute(self, context):
        scn = context.scene
        create_placeholders(scn)

        self.report({'INFO'}, "Placeholders created")
        
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_OT_create_placeholders)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_OT_create_placeholders)