import bpy

# image inspector panel
class DUPERENDER_PT_main_panel(bpy.types.Panel):
    bl_label = "Dupe Render"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        scn = context.scene
        self.layout.prop(scn, "duperender_use_duperender", text="")

    def draw(self, context):
        scn = context.scene
        
        layout = self.layout

        if not scn.duperender_use_duperender:
            layout.enabled = False
        layout.use_property_split = True

        layout.operator("duperender.hash_frame")

        layout.operator("duperender.preview_dupe_render", text="Preview Dupes for scene range").custom_range = False

        col = layout.column(align=True)
        col.prop(scn, "duperender_custom_frame_start")
        col.prop(scn, "duperender_custom_frame_end", text="End")
        
        layout.operator("duperender.preview_dupe_render", text="Preview Dupes for custom range").custom_range = True

        layout.prop(scn, "duperender_to_render_list")


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_PT_main_panel)