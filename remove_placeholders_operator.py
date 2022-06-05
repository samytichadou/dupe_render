import bpy
import os


def remove_single_placeholder(scene, frame_number):
    path = scene.render.frame_path(frame=frame_number)
    if os.path.isfile(path):
        if os.path.getsize(path)!=0:
            print("Dupe Render --- frame %i is not a placeholder, skipping" % frame_number)
            return False
        try:
            os.remove(path)
            print("Dupe Render --- frame %i removed" % frame_number)
            return True
        except OSError as error:
            print(error)
            print("Dupe Render --- unable to remove frame %i, skipping" % frame_number)
            return False
    else:
        print("Dupe Render --- frame %i does not exist" % frame_number)
        return False

def remove_dupe_placeholders(scene, scene_range):
    dupe_list = scene.duperender_dupelist.split(",")
    for dupe in dupe_list:
        i = int(dupe)
        if not scene_range \
        or i in range(scene.frame_start, scene.frame_end+1):
            remove_single_placeholder(scene, i)

def remove_placeholders(scene, scene_range):
    if scene_range:
        frame_range=range(scene.frame_start, scene.frame_end+1)
    else:
        frame_range=range(scene.duperender_frame_start, scene.duperender_frame_end+1)
    for i in frame_range:
        remove_single_placeholder(scene, i)


class DUPERENDER_OT_remove_placeholders(bpy.types.Operator):
    bl_idname = "duperender.remove_placeholders"
    bl_label = "Remove placeholders"
    bl_description = "Remove Dupe frames placeholders previously created"
    #bl_options = {'INTERNAL'}

    scene_range : bpy.props.BoolProperty(
        name = "Scene Frame Range",
        description="Remove placeholders in the scene frame range",
        default=True,
        )

    all_frames : bpy.props.BoolProperty(
        name = "All frames",
        description="Remove all frames, not only dupe frames",
        )

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        row=layout.row()
        row.prop(self, "scene_range")
        row.prop(self, "all_frames")

        box=layout.box()
        col=box.column(align=True)
        col.label(text="Proceed with caution", icon="ERROR")
        col.label(text="This action will remove existing dupe placeholders")
        col.label(text="Are you sure ?")  

    def execute(self, context):
        scn = context.scene
        if self.all_frames:
            remove_placeholders(scn, self.scene_range)
        else:
            remove_dupe_placeholders(scn, self.scene_range)

        self.report({'INFO'}, "Placeholders removed")
        
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_OT_remove_placeholders)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_OT_remove_placeholders)