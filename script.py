import bpy
import csv
from bpy import context

frame_tick = 7.5729
delay = 29
object = 'Bass 3'
animation = 'Bass3'
channel = "4"
note = " 60"
frame = 0
animlength = 69
lastframe = (int(animlength) * -1 - 1)
bpy.data.objects[object].select = True
bpy.context.area.type = 'NLA_EDITOR'

def nlaselect():
    ob = context.object
    ad = ob.animation_data
    if ad:
        for i, track in enumerate(ad.nla_tracks):
            # select all whose name starts with "Nla"
            track.select = track.name.startswith("Nla")
            # make active track if in pos 0
            if track.select and not i:
                ad.nla_tracks.active = track
                
nlaselect()

def dupe(row):
    bpy.ops.object.duplicate()

    print(bpy.context.selected_objects)

    bpy.context.area.type = 'NLA_EDITOR'

    for obj in bpy.context.selected_objects:
        obj.animation_data_clear()          #clear animation data
        bpy.ops.nla.selected_objects_add()  #add blank animation data
        obj.animation_data.nla_tracks.new() #add new NLA track
    print("animation cleaned.")

    bpy.ops.anim.channels_select_all_toggle()

    nlaselect()
                
    bpy.context.scene.frame_set((int(row[1])/frame_tick - delay + 39))
    bpy.ops.nla.actionclip_add(action=animation)
    print("added animation to dupe.")
    bpy.context.area.type = 'TEXT_EDITOR'
        
def nodupe(row):
    bpy.context.area.type = 'NLA_EDITOR'  
    print("no note overlap, continuing as normal.")
    bpy.context.scene.frame_set((int(row[1])/frame_tick - delay + 39))
    bpy.ops.nla.actionclip_add(action=animation)
    bpy.context.area.type = 'TEXT_EDITOR'
        
def keyframe(row):
    global frame
    global lastframe
    print(lastframe)
    print(frame)
    print(animlength)
    if lastframe > (frame - animlength):
        dupe(row)
    else:
        nodupe(row)


def main():
    
    global frame
    global lastframe
    with open("pd3.csv", "rt", encoding="ascii") as ifile:
        read = csv.reader(ifile, delimiter = ',', quotechar = "'")
        print("opened file.")
        for row in read :
            if row[0] == channel and row[2] == " Note_on_c" and row[4] == note and row[1] != 0:
                print("conditions met.")
                frame = (int(row[1]) / frame_tick)
                print("frame: " + str(frame))
                keyframe(row)
                lastframe = (int(row[1]) / frame_tick)
                continue
            else:
                continue
			
		
if __name__ == "__main__":

    main()
    bpy.context.area.type = 'NLA_EDITOR'
    bpy.ops.anim.channels_select_all_toggle()
    bpy.ops.nla.select_all_toggle(invert=False)
    bpy.context.area.type = 'VIEW_3D'
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.context.area.type = 'TEXT_EDITOR'
