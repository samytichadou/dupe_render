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


        if not scn.duperender_use_duperender\
        or scn.render.use_overwrite:
            layout.enabled = False

        if scn.render.use_overwrite:
            layout.label(text="Overwrite Render used", icon = "ERROR")

        layout.operator("duperender.hash_frame")
        layout.operator("duperender.process_dupe_render")

        box = layout.box()
        box.prop(scn, "duperender_next_render")
        row = box.row()
        if not scn.duperender_next_render:
            row.enabled = False
        row.prop(scn, "duperender_dupelist")


### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_PT_main_panel)