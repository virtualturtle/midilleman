import bpy
import csv

frame_tick = 7.5729
delay = 30
object = 'Bass 3'
animation = 'Bass3'
channel = 4
note = " 60"
frame = 0
animlength = 69
lastframe = (int(animlength) * -1 - 1)
bpy.data.objects[object].select = True

def keyframe(row):
    
    global object
    global frame
    global lastframe
    print(lastframe)
    print(frame)
    print(animlength)
    if lastframe > (frame - animlength):
        
        print("Note Overlap by " + str((frame - lastframe) * 1 ) + " frames. Duplicating.")
        bpy.ops.object.duplicate()
        print(object)
        object = bpy.context.selected_objects
        for obj in bpy.context.selected_objects:
            obj.animation_data_clear()
        bpy.context.area.type = 'VIEW_3D'
        #bpy.data.objects[object].select = True
        #bpy.context.scene.objects.active = bpy.data.objects[object]
        bpy.context.area.type = 'NLA_EDITOR'
        bpy.context.scene.frame_set(int(row[1])/frame_tick)
        bpy.ops.nla.actionclip_add(action=animation)
        bpy.context.area.type = 'TEXT_EDITOR'
    else:
        print("no note overlap, continuing as normal.")
        #bpy.data.objects[object].select = True
        #bpy.context.scene.objects.active = bpy.data.objects[object]
        bpy.context.area.type = 'NLA_EDITOR'
        bpy.context.scene.frame_set(int(row[1])/frame_tick)
        bpy.ops.nla.actionclip_add(action=animation)
        bpy.context.area.type = 'TEXT_EDITOR'


def main():
    
    global frame
    global lastframe
    with open("pd3.csv", "rt", encoding="ascii") as ifile:
        read = csv.reader(ifile, delimiter = ',', quotechar = "'")
        print("opened file.")
        for row in read :
            #print("reading line.")
            if row[0] == "4" and row[2] == " Note_on_c" and row[4] == note and row[1] != 0:
                print("conditions met.")
                frame = (int(row[1]) / frame_tick)
                print("frame: " + str(frame))
                keyframe(row)
                lastframe = (int(row[1]) / frame_tick)
                continue
            else:
                #print("nope.")
                continue
			
		
if __name__ == "__main__":
    main()
