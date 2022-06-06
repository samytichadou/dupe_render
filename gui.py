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

        bigcol = layout.column(align=True)

        # render infos box
        box = layout.box()
        if not scn.duperender_render:
            box.enabled = False
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
        if not scn.duperender_is_processed:
            row.label(text="Dupes not processed", icon = "ERROR")
        elif scn.duperender_frame_start>scn.frame_start\
            or scn.duperender_frame_end<scn.frame_end:
            row.label(text="Range superior to processed frames", icon = "ERROR")
        elif scn.duperender_frame_start!=scn.frame_start\
            or scn.duperender_frame_end!=scn.frame_end:
            row.alert=False
            row.label(text="Range changed, could cause problems", icon = "INFO")
        elif scn.duperender_dupelist == "":
            row.alert=False
            row.label(text="No dupe frames", icon = "INFO")
        else:
            row.alert=False
            row.label(text="Dupes OK", icon = "CHECKMARK")

        col.separator()
        col.operator("duperender.find_dupe_frames")

        # Dupes infos
        if scn.duperender_is_processed:
            col.separator()
            row = col.row()
            row.alignment='CENTER'
            row.operator(
                "duperender.infos_popup",
                icon="INFO",
                text="%i/%i Originals    -    %i Dupes    -    %i%% Gain"\
                    % (scn.duperender_nb_fr_to_render, scn.duperender_nb_fr_total,\
                    scn.duperender_nb_dupes_fr, scn.duperender_gain),
                emboss=False,
            )

        #col.operator("duperender.hash_frame")

        # manual op
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Manual Frame Operations")
        col.separator()
        col.operator("duperender.create_placeholders")
        col.operator("duperender.remove_placeholders")
        col.separator()
        col.operator("duperender.duplicate_originals")


class DUPERENDER_OT_infos_popup(bpy.types.Operator):
    bl_idname = "duperender.infos_popup"
    bl_label = "Show Infos"
    bl_description = "Show Infos about current Dupe process"
    bl_options = {'INTERNAL'}

    modify_dupes : bpy.props.BoolProperty(
        name = "Modify Dupes",
        )

    modify_originals : bpy.props.BoolProperty(
        name = "Modify Originals",
        )

    @classmethod
    def poll(cls, context):
        return context.scene.duperender_is_processed

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)
 
    def draw(self, context):
        scn=context.scene

        layout = self.layout
        
        col=layout.column(align=True)
        
        row = col.row()
        split = row.split()
        split.label(text="Processed Range")
        split.alignment='RIGHT'
        split.label(text="%i-%i" % (scn.duperender_frame_start, scn.duperender_frame_end))

        row = col.row()
        split = row.split()
        split.label(text="Processed Date")
        split.alignment='RIGHT'
        split.label(text=scn.duperender_processing_date)

        col.label(text="%i Dupes" % scn.duperender_nb_dupes_fr)
        col.label(text="%i Originals" % scn.duperender_nb_fr_to_render)

        col.separator()

        box=col.box()
        row=box.row(align=True)
        row.alignment="LEFT"
        row.label(text="Dupes    ")
        row.separator()
        row.prop(self, "modify_dupes", text="", icon="GREASEPENCIL")
        subrow=row.row(align=True)
        row.alignment="EXPAND"
        if not self.modify_dupes:
            subrow.enabled=False
        subrow.prop(scn, "duperender_dupelist", text="")
        grid = box.grid_flow(row_major=True, columns=15, align=True)
        for i in scn.duperender_dupelist.split(","):
            grid.label(text=i)
        
        box=col.box()
        row=box.row(align=True)
        row.alignment="LEFT"
        row.label(text="Originals")
        row.separator()
        row.prop(self, "modify_originals", text="", icon="GREASEPENCIL")
        subrow=row.row(align=True)
        row.alignment="EXPAND"
        if not self.modify_originals:
            subrow.enabled=False
        subrow.prop(scn, "duperender_originallist", text="")
        grid = box.grid_flow(row_major=True, columns=15, align=True)
        for i in scn.duperender_originallist.split(","):
            grid.label(text=i)

    def execute(self, context):       
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_PT_main_panel)
    bpy.utils.register_class(DUPERENDER_OT_infos_popup)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_PT_main_panel)
    bpy.utils.unregister_class(DUPERENDER_OT_infos_popup)