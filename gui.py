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
        row = col.row()
        row.alert=True
        if scn.render.is_movie_format:
            row.label(text="Movie Format Output used", icon = "ERROR")
        elif scn.render.use_overwrite:
            row.label(text="Overwrite Render used", icon = "ERROR")
        elif scn.duperender_dupelist == "":
            row.label(text="No dupe frames", icon = "ERROR")
        elif scn.duperender_frame_start==-1 and scn.duperender_frame_end==-1:
            row.label(text="No processed range", icon = "ERROR")
        elif scn.duperender_frame_start>scn.frame_start\
            or scn.duperender_frame_end<scn.frame_end:
            row.label(text="Range superior to processed frames", icon = "ERROR")
        elif scn.duperender_frame_start!=scn.frame_start\
            or scn.duperender_frame_end!=scn.frame_end:
            row.label(text="Range changed, could cause problems", icon = "INFO")
        else:
            row.alert=False
            row.label(text="Ready", icon = "CHECKMARK")
        col.separator()
        row = col.row()
        row.label(text="Render Settings")
        row.prop(scn.render.image_settings, "file_format", text="")
        row.prop(scn.render, "use_overwrite")

        # process box
        box = bigcol.box()
        col = box.column(align=True)
        col.operator("duperender.find_dupe_frames")

        if scn.duperender_frame_start!=-1 and scn.duperender_frame_end!=-1:
            col.label(text="Processed Range : %i-%i" % (scn.duperender_frame_start, scn.duperender_frame_end))
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