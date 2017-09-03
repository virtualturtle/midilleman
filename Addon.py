import bpy

def midi_select(self, context):
    last_select = context.scene.midi_enum.pop()
    context.scene.midi_enum.add(last_select)
    print('called and changed to', last_select, ' / ', context.scene.midi_enum)

class MidillemanPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Midilleman"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.prop(scene, "midi_enum", expand=False)

def register():
    bpy.types.Scene.midi_enum = bpy.props.EnumProperty(
        name = "Single or multiple midi(s):",
        description = "Single track or multi-tracked midi file",
        items = [
            ("0" , "Single track" , "Single midi track"),
            ("1", "Multiple tracks", "Multiple midi tracks")
        ],
        options = {"ENUM_FLAG"},
        update = midi_select
    )

    bpy.utils.register_class(MidillemanPanel)

def unregister():
    bpy.utils.unregister_class(MidillemanPanel)
    del bpy.types.Scene.midi_enum


if __name__ == "__main__":
    register()


ICONS:

CHECKBOX_DEHLT uncheckedbox
CHECKBOX_HLT   checkedbox
FILESEL        select a file (midi)
ZOOMIN         (plus) Add a channel
X              (X) Delete a channel
TRIA_RIGHT     (>) collapse channel
TRIA_DOWN      (v) expand channel
SOUND          (music mote) select note
