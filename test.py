import bpy

bpy.ops.object.duplicate()

print(bpy.context.selected_objects)

bpy.context.area.type = 'NLA_EDITOR'

#for obj in bpy.context.selected_objects:
    #obj.animation_data_clear()          #clear animation data
    #bpy.ops.nla.selected_objects_add()  #add blank animation data
    #obj.animation_data.nla_tracks.new() #add new NLA track
print("animation cleaned.")
bpy.ops.nla.tracks_delete()
for obj in bpy.context.selected_objects:
    obj.animation_data.nla_tracks.new()
bpy.ops.nla.actionclip_add(action='CubeAction')
bpy.ops.anim.channels_select_all_toggle()

#print("added animation to dupe.")

bpy.context.area.type = 'TEXT_EDITOR'

#print("no note overlap, continuing as normal.")
#bpy.context.scene.frame_set(int(row[1])/frame_tick)
bpy.ops.nla.actionclip_add(action=animation)
