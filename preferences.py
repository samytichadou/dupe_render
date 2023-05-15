import bpy
import os

addon_name=os.path.basename(os.path.dirname(__file__))
command_string='blender -b filepath.blend --python-expr "import bpy;bpy.ops.duperender.process_dupes_bg()"'

class DUPERENDER_PF_preferences(bpy.types.AddonPreferences) :
    bl_idname = addon_name

    command: bpy.props.StringProperty(
        name="Command",
        default=command_string,
        )

    def draw(self, context) :
        wm = context.window_manager
        layout = self.layout
        layout.label(
            text="Background Dupe Process Command",
            icon="INFO",
            )
        col=layout.column(align=True)
        col.label(text=command_string)
        col.prop(self, "command", text="")

# get addon preferences
# def get_addon_preferences():
#     addon = bpy.context.preferences.addons.get(addon_name)
#     return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(DUPERENDER_PF_preferences)
def unregister():
    bpy.utils.unregister_class(DUPERENDER_PF_preferences)
