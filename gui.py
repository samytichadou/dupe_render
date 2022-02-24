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

    # def draw_header(self, context):
    #     scn = context.scene
    #     self.layout.prop(scn, "duperender_use_duperender", text="")

    def draw(self, context):
        scn = context.scene
        layout = self.layout


        if not scn.duperender_use_duperender:
            layout.enabled = False

        if context.scene.render.is_movie_format:
            layout.label(text="Movie Format Output used", icon = "INFO")
        elif scn.render.use_overwrite:
            layout.label(text="Overwrite Render used", icon = "INFO")
        elif scn.duperender_dupelist == "":
            layout.label(text="No dupe frames", icon = "INFO")

        box = layout.box()
        col = box.column(align=True)
        col.operator("duperender.find_dupe_frames")
        col.prop(scn, "duperender_next_render")
        # row = col.row()
        # if not scn.duperender_next_render:
        #     row.enabled = False
        col.prop(scn, "duperender_dupelist", text="Dupes")
        col.prop(scn, "duperender_originallist", text="Originals")

        box = layout.box()
        col = box.column(align=True)
        col.operator("duperender.hash_frame")


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_PT_main_panel)