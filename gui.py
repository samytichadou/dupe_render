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
        self.layout.prop(scn, "duperender_render", text="")

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        # if not scn.duperender_use_duperender:
        #     layout.enabled = False
        if not scn.duperender_render:
            layout.enabled = False

        bigcol = layout.column(align=True)

        # render infos box
        box = bigcol.box()
        col = box.column(align=True)
        if scn.render.is_movie_format:
            col.label(text="Movie Format Output used", icon = "INFO")
        elif scn.render.use_overwrite:
            col.label(text="Overwrite Render used", icon = "INFO")
        elif scn.duperender_dupelist == "":
            col.label(text="No dupe frames", icon = "INFO")
        else:
            col.label(text="All set", icon = "CHECKMARK")
        col.separator()
        col.prop(scn.render.image_settings, "file_format")
        col.prop(scn.render, "use_overwrite")

        # process box
        box = bigcol.box()
        col = box.column(align=True)
        col.operator("duperender.find_dupe_frames")

        col.prop(scn, "duperender_dupelist", text="Dupes")
        col.prop(scn, "duperender_originallist", text="Originals")

        # options box
        box = bigcol.box()
        col = box.column(align=True)
        col.operator("duperender.hash_frame")


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_PT_main_panel)