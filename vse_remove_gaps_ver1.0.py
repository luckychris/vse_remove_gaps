bl_info = {
    "name": "Remove Gaps in VSE",
    "description": "Removes all gaps between strips in the Video Sequence Editor",
    "author": "Blender.Fun",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Sequencer > Sidebar > Remove Gaps",
    "category": "Sequencer",
}

import bpy

addon_keymaps = []

def remove_gaps():
    scene = bpy.context.scene
    sequences = list(scene.sequence_editor.sequences_all)

    sequences.sort(key=lambda s: (s.channel, s.frame_start))
    channel_ends = {}

    for seq in sequences:
        ch = seq.channel
        if ch not in channel_ends:
            channel_ends[ch] = 0

        if seq.frame_start > channel_ends[ch]:
            gap = seq.frame_start - channel_ends[ch]
            seq.frame_start -= gap

        channel_ends[ch] = seq.frame_start + seq.frame_final_duration

class VSE_OT_RemoveGaps(bpy.types.Operator):
    """Remove Gaps in VSE"""
    bl_idname = "vse.remove_gaps"
    bl_label = "Remove Gaps"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.scene.sequence_editor:
            self.report({'WARNING'}, "No sequence editor found.")
            return {'CANCELLED'}
        remove_gaps()
        return {'FINISHED'}

class VSE_PT_RemoveGapsPanel(bpy.types.Panel):
    """Creates a Panel in the VSE UI"""
    bl_label = "Remove Gaps"
    bl_idname = "SEQUENCER_PT_remove_gaps"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Remove Gaps"

    def draw(self, context):
        layout = self.layout
        layout.operator("vse.remove_gaps")

def register():
    bpy.utils.register_class(VSE_OT_RemoveGaps)
    bpy.utils.register_class(VSE_PT_RemoveGapsPanel)

    # Add shortcut
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Sequencer', space_type='SEQUENCE_EDITOR')
    kmi = km.keymap_items.new("vse.remove_gaps", type='BACK_SPACE', value='PRESS', ctrl=True, oskey=True)
    addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(VSE_OT_RemoveGaps)
    bpy.utils.unregister_class(VSE_PT_RemoveGapsPanel)

if __name__ == "__main__":
    register()
