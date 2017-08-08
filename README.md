# Midilleman
Converting MIDI to blender NLA for music-generated animation
<pre>
___  ___ _      _  _  _  _                                
|  \/  |(_)    | |(_)| || |                               
| .  . | _   __| | _ | || |  ___  _ __ ___    __ _  _ __  
| |\/| || | / _` || || || | / _ \| '_ ` _ \  / _` || '_ \ 
| |  | || || (_| || || || ||  __/| | | | | || (_| || | | |
\_|  |_/|_| \__,_||_||_||_| \___||_| |_| |_| \__,_||_| |_|
</pre>                                                          

## Resources/References

### Midi to blender:
https://github.com/stephanpieterse/pyblend-animidi
https://www.fourmilab.ch/webtools/midicsv/
http://blendit.xaa.pl/index.php?p=middrv&l=eng
https://blenderartists.org/forum/showthread.php?411135-MIDI-Keyboard-Controlling-Blender-Face

### Blender Addon references:
https://docs.blender.org/api/blender_python_api_2_65_5/info_tutorial_addon.html
https://www.blendernation.com/2016/10/18/blender-addon-programming-tutorial/
https://michelanders.blogspot.com/p/creating-blender-26-python-add-on.html

https://blender.stackexchange.com/questions/39854/how-can-i-open-a-file-select-dialog-via-python-to-add-an-image-sequence-into-vse Adding an “open csv file” button

### Selecting an object: (not sure if correct. This selects the object in the scene, not sure about if it's for applying modifiers to) we want “Browse object to be linked”
https://docs.blender.org/api/blender_python_api_2_78b_release/bpy.ops.outliner.html#bpy.ops.outliner.object_operation

### Adding preset animations to an object
https://docs.blender.org/api/blender_python_api_2_78b_release/bpy.ops.nla.html#bpy.ops.nla.actionclip_add

### Offsetting in NLA editor:
https://www.youtube.com/watch?v=EWX0e1tyV5w

### Seeing NLA action properties (frame count etc):
https://docs.blender.org/manual/en/dev/editors/nla/properties_modifiers.html#action-clip

### Good resource for NLA python:
http://blendersushi.blogspot.com/2013/05/python-nla-non-linear-animation-with.html
------------------------------------------------------
## Functionality:

### Use Midi Channel:
	After Parsing csv file, determine the channels and allow for selection

### Listen To:
	In each Channel, allow for selection of one specific note/percussion instrument

### Apply To:
	Select object or armature to use, whichever was entered

### Use Animation:
	Select action from the selected object's Action Editor
### Actions can be Object location/rotation/scale, Armature animation, or shader nodetrees (useful for lasers)

### Offset frames:
	In the action editor, apply the entered amount as a translation in frames, for example: if -38 was entered, shift the selected object’s animation 38 frames backwards.

### Alternate:
	By numbering each note chronologically, 1,2,3... select two blender channels, one for the odds and one for the evens. This could be expanded to alternate between more than two.

### Extra note:
If a note is hit again before its animation is finished, duplicate the object, clear its animations and put the second animation there, to prevent overlap. Possibly use that object multiple times instead of duplicating each time. This issue could probably be solved if we used alternation between two objects per channel. This is especially noticeable with the drums, seeing as they will most likely be hit more than once per animation cycle.
		Functionality: read action lengths of each object. Attach framecount variable to each object. Whenever the note is played, check that many frames and under to determine if duplicates exist. For example, Bass4 has a framecount of 72, so when it’s played in the csv, check between frame +0 and frame +72, if there is another of the same note, trigger the duplication/alternation.

### Resting:
	For example, an armature (bones but acts the same way as objects do in the action editor) would be used, let’s take the robot from starship groove. Each unique note it hits would be a separate animation (13 actions total), which is implemented, however the transition between them is not. User will create an action for resting (1 frame. Do a check to make sure that it is 1 frame). If resting is checked, there’ll be a resting threshold that determines to amount of frames in between the played animation and the resting frame. Let’s say we hit two notes right after each other and we give it a resting threshold of 10 frames.
Apply a transition strip during the threshold (https://docs.blender.org/manual/en/dev/editors/nla/strips.html#transition-strips)
||||||||||||..........|...............|..........|||||||||
Note Animation Resting Threshold Resting Action Empty Frame
If the resting threshold exceeds the amount of frames available (threshold*2 +1), take an average of the first and last frames of each animation use that frame, round up if not a whole number. 
||||||||||......|......|||||||||
Resting is applied after the initial application of animations to avoid overlap.


### Apply:
	Bake all notes to actions, use progress bar at the top for added debug

### Refresh:
	Delete all actions and rebake OR scan midis for differences and apply differences.
------------------------------------------------------
## Pipe Dream Notes:

Bass1 		F	29
Bass2 		G	31
Bass3 		Bb	34
Bass4 		C	36
Bass5 		Fb	40
Bass6 		F	41
Bass7		G	43
Bass8 		Bb	46
Bass9 		C	48
Bass10 	D	50
Bass11 	Fb	52
Bass12 	G	55

Treble1	D	62
Treble2	Bb	58
Treble3	A	57
Treble4	G	55
------------------------------------------------------
## Workflow:
### Setup

Select midi files
Parse midi files to allow selection of channels and notes (record which channel #s are active and what note #s are active)
Convert Active Numbers to Letter Notes, 36 = C
Select channels, notes.
Allow for renaming of active Channels to instrument names
Select objects to apply them to.
Select NLA actions to apply to objects.
Set offset for each one.
Start at frame 0 in midi
Start at frame 0 in blender  bpy.context.scene.frame_set(0)
Attach note variable and animation variable to each object
Each channel in blender contains:
Csv instrument identifier
Csv Note identifier


### Main Loop:

Go to next frame that has midi action
Set that frame in blender bpy.context.scene.frame_set(whatever that number is)
Find what channel it’s on
Find What note it is
Based on the note and what was entered in setup, select the object that corresponds to the note using bpy.data.objects['ENTEREDOBJECTNAME'].select = True
Whatever the offset entered in setup was, take the current frame and add the offset to it using bpy.context.scene.frame_set(whatever that number is)
Using the Action entered in setup, apply the action to the selected object bpy.ops.nla.actionclip_add(whatever the user selected in setup)
Resume to non-offset frame
Move to next active frame in Midi
Move to same frame in blender bpy.context.scene.frame_set(whatever that number is)

Repeat until last Midi frame has been completed


Rendering:

	Cycles Filmic with denoise. 64 or 128 samples
Local rendering: ~5 Days for 7777 frames
Sheep-it rendering: 2.5 days and under, reported up to 40x speedup meaning a 3 hour render


import csv
>>> with open('eggs.csv', 'rb') as csvfile:
...    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
...    for row in spamreader:
...        print ', '.join(row)

https://docs.python.org/2/library/csv.html

Top of file: @ tick (time to trigger), channel (channel to look in), note (note in that channel to hit
Ex.: 32, 0, 36

