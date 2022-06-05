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
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Render Settings")
        # Render settings Infos
        row = col.row()
        row.alert=True
        if scn.render.is_movie_format:
            row.label(text="Movie Format Output used", icon = "ERROR")
        elif scn.render.use_overwrite:
            row.label(text="Overwrite Render used", icon = "ERROR")
        elif scn.render.use_placeholder:
            row.label(text="Placeholder used, could cause problems in farm", icon = "ERROR")
        else:
            row.alert=False
            row.label(text="Settings OK", icon = "CHECKMARK")
        
        col.separator()
        row = col.row()
        row.prop(scn.render.image_settings, "file_format", text="")
        row.prop(scn.render, "use_overwrite")
        row.prop(scn.render, "use_placeholder")

        # process box
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Frames Process")
        # Dupe range Infos
        row = col.row()
        row.alert=True
        if scn.duperender_dupelist == "":
            row.label(text="No dupe frames", icon = "ERROR")
        elif scn.duperender_frame_start==-1 and scn.duperender_frame_end==-1:
            row.label(text="No processed range", icon = "ERROR")
        elif scn.duperender_frame_start>scn.frame_start\
            or scn.duperender_frame_end<scn.frame_end:
            row.label(text="Range superior to processed frames", icon = "ERROR")
        elif scn.duperender_frame_start!=scn.frame_start\
            or scn.duperender_frame_end!=scn.frame_end:
            row.alert=False
            row.label(text="Range changed, could cause problems", icon = "INFO")
        else:
            row.alert=False
            row.label(text="Dupes OK", icon = "CHECKMARK")

        if scn.duperender_nb_fr_to_render!=-1:
            row = col.row()
            split = row.split()
            split.label(text="%i/%i Frame(s) to Render" % (scn.duperender_nb_fr_to_render, scn.duperender_nb_fr_total))
            if scn.duperender_gain!=-1:
                split.alignment='RIGHT'
                split.label(text="%i%% Render Gain" % scn.duperender_gain)

        col.separator()
        col.operator("duperender.find_dupe_frames")

        col.separator()
        if scn.duperender_frame_start!=-1 and scn.duperender_frame_end!=-1:
            row = col.row()
            split = row.split()
            split.label(text="Processed Range")
            split.alignment='RIGHT'
            split.label(text="%i-%i" % (scn.duperender_frame_start, scn.duperender_frame_end))
        if scn.duperender_processing_date:
            row = col.row()
            split = row.split()
            split.label(text="Processed Date")
            split.alignment='RIGHT'
            split.label(text=scn.duperender_processing_date)
        col.separator()
        col.prop(scn, "duperender_dupelist", text="Dupes")
        col.prop(scn, "duperender_originallist", text="Originals")
        #col.operator("duperender.hash_frame")
        col.separator()
        col.operator("duperender.create_placeholders")
        col.operator("duperender.duplicate_originals")


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_PT_main_panel)