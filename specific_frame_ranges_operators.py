import bpy


class DUPERENDER_OT_add_frame_range(bpy.types.Operator):
    bl_idname = "duperender.add_frame_range"
    bl_label = "Add Frame Range"
    bl_description = "Add specific frame range as dupe or original"
    #bl_options = {'INTERNAL'}

    frame_start : bpy.props.IntProperty(
        name = "Range Start Frame",
        default=-1,
        )
    frame_end : bpy.props.IntProperty(
        name = "Range End Frame",
        default=-1,
        )
    range_items = [
        ("DUPE", "Dupe", ""),
        ("ORIGINAL", "Original", ""),
        ]
    range_type : bpy.props.EnumProperty(
        name = "Range Type",
        items = range_items,
        default = "DUPE",
        )
    is_frame_start_dupe : bpy.props.BoolProperty(
        name = "Start Frame Dupe",
        description = "Is Start Frame a Dupe, if False, considered Original",
        )

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        scn = context.scene
        if self.frame_start == -1:
            self.frame_start = scn.frame_start
        if self.frame_end == -1:
            self.frame_end = scn.frame_end
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "range_type", text="")#, expand=True)
        row = layout.row()
        if self.range_type == "ORIGINAL":
            row.enabled = False
        row.prop(self, "is_frame_start_dupe")

        col = layout.column(align=True)
        col.prop(self, "frame_start")
        col.prop(self, "frame_end")

    def execute(self, context):
        # Check if valid range
        if self.frame_start > self.frame_end:
            self.report({'WARNING'}, "Invalid Frame Range")
            return {'CANCELLED'}

        range_collection = context.scene.duperender_properties.specific_ranges

        # Create entry
        new_range = range_collection.add()
        if self.range_type == "DUPE" and not self.is_frame_start_dupe:
            new_range.frame_start = self.frame_start + 1
        else:
            new_range.frame_start = self.frame_start
        new_range.frame_end = self.frame_end
        new_range.type = self.range_type

        # Refresh UI
        for area in context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "Range Created")

        return {'FINISHED'}

class DUPERENDER_OT_remove_frame_range(bpy.types.Operator):
    bl_idname = "duperender.remove_frame_range"
    bl_label = "Remove Frame Range"
    bl_description = "Remove specific frame range"
    #bl_options = {'INTERNAL'}

    index : bpy.props.IntProperty()
    all : bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return context.scene.duperender_properties.specific_ranges

    def execute(self, context):
        range_collection = context.scene.duperender_properties.specific_ranges

        # Check if valid index
        if not self.all:
            try:
                range_collection[self.index]
            except IndexError:
                self.report({'INFO'}, "Invalid Range Entry")
                return {'CANCELLED'}
            range_collection.remove(self.index)

        else:
            range_collection.clear()

        # Refresh UI
        for area in context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "Range(s) Removed")

        return {'FINISHED'}

### REGISTER ---

def register():
    bpy.utils.register_class(DUPERENDER_OT_add_frame_range)
    bpy.utils.register_class(DUPERENDER_OT_remove_frame_range)

def unregister():
    bpy.utils.unregister_class(DUPERENDER_OT_add_frame_range)
    bpy.utils.unregister_class(DUPERENDER_OT_remove_frame_range)
