import bpy
import os


def remove_placeholders(scene):
    dupe_list = scene.duperender_dupelist.split(",")

    for dupe in dupe_list:
        i = int(dupe)
        path = scene.render.frame_path(frame=i)
        #remove dupe frame
        if os.path.isfile(path):
            #check if placeholder
            if os.path.getsize(path)!=0:
                print("Dupe Render --- frame %i is not a placeholder, skipping" % i)
                continue
            try:
                os.remove(path)
                print("Dupe Render --- frame %i removed" % i)
            except OSError as error:
                print(error)
                print("Dupe Render --- unable to remove frame %i, skipping" % i)
                continue
        else:
            print("Dupe Render --- frame %i does not exist" % i)


class DUPERENDER_OT_remove_placeholders(bpy.types.Operator):
    bl_idname = "duperender.remove_placeholders"
    bl_label = "Remove placeholders"
    bl_description = "Remove Dupe frames placeholders previously created"
    #bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.scene.duperender_dupelist!=""

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text="Proceed with caution", icon="ERROR")
        col=layout.column(align=True)
        col.label(text="This action will remove existing dupe placeholders")
        col.label(text="Are you sure ?")  

    def execute(self, context):
        scn = context.scene
        remove_placeholders(scn)

        self.report({'INFO'}, "Placeholders removed")
        
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_OT_remove_placeholders)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_OT_remove_placeholders)