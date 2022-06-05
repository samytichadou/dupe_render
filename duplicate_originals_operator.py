import bpy

from .handler import create_placeholders


class DUPERENDER_OT_duplicate_originals(bpy.types.Operator):
    bl_idname = "duperender.duplicate_originals"
    bl_label = "Duplicate originals"
    bl_description = "Create empty files for detected Dupe frames"
    #bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.scene.duperender_dupelist!=""

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text="This action will create placeholders", icon="ERROR")
        layout.label(text="Are you sure ?")  

    def execute(self, context):
        scn = context.scene
        create_placeholders(scn)

        self.report({'INFO'}, "Placeholders created")
        
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_OT_duplicate_originals)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_OT_duplicate_originals)