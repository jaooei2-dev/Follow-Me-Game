<<<<<<< HEAD
import maya.cmds as cmds
import time
import random
import os
import maya.mel as mel

NOTE_COLOS = {
	"Do" : (1,0,0),
	"Re" : (1,0.5,0),
	"Mi" : (1,1,0),
	"Fa" : (0,1,0),
	"Sol" : (0,0,1),
	"La" : (1,0,1),
	"Ti" : (0.5,0,1),
}

SOUND_DIR = 

GRAY = (0.5, 0.5, 0.5)

def Create_object():
	clear_scene()
	spacing = 4
	objetcts = []
	note_name = list(NOTE_COLOS.keys())
	
	shape_functions = [
		lambda: cmds.polySphere(name='Do_note')[0],
		lambda: cmds.polyCube(name='Re_note')[0],
		lambda: cmds.polyCone(name='Mi_note')[0],
		lambda: cmds.polyCylinder(name='Fa_note')[0],
		lambda: cmds.polyTorus(name='Sol_note')[0],
		lambda: cmds.polyPyramid(name='La_note')[0],
		lambda: cmds.polyPlane(name='Ti_note')[0],
	]

	for i, note in enumerate(note_names):
		obj = shape_functions[i]()
		cmds.move(i * spacing, 0, 0, obj)
		set_color(obj, GRAY)
		objetcts.append((obj, note))
	return objetcts

def set_color(obj, rgb):
	shape = cmds.listRelatives(obj, shapes=True)
	shader = cmds.shadingNode('lambert', asShader=True, name=f'{obj}_shader')
	sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{obj}_SG')
	cmds.connectAttr(f'{shader}.outColor', f'{sg}.noSurfaceShader', force=True)
	cmds.setAttr(f'{shader}.color', *rgb, type='double3')
	cmds.sets(obj, e=True, forceElement=sg)

def blink_object(obj, note, duration=0.5):
	color = NOTE_COLOS[note]
	shape = cmds.listRelatives(obj, shapes=True)[0]
	shader = cmds.listConnetctions(shape, type='lembert')[0]
	cmds.setAttr(f'{shader}.color', *color, type='double3')
	cmds.refresh()
	play_note(note)
	time.sleep(duration)
	cmds.setAttr(f'{shader}.color', *GRAY, type='double3')
	cmds.refresh()

def play_note(note):
	path = os.path.join(SOUND_DIR, f'{note}.wav').replace('\\','/')
	if os.path.exsits(path):
		mel.eval(f'sound -p 0 -file '{path}';')
	else:
		print (f'Sound file for {note} not found: {path}')

def shuffle_object_positions(objetcts, spacing=4):
	position = [cmds.xform(obj[0], q=True, ws=True, t=True) for obj in objetcts]
	random.shuffle(position)
	for i, (obj, _) in  enumerate(objetcts):
		cmds.xform(obj, ws=True, t=position[i])

def clear_scene():
	objs = cmds.ls('*_note')
	if objs:
		cmds.delete(objs)
=======
import maya.cmds as cmds
import random
import time
import os
import maya.mel as mel

NOTE_COLORS = {
    'Do': (238, 0, 0),
    'Re': (255, 127, 0),
    'Mi': (255, 215, 0),
    'Fa': (0, 238, 0),
    'Sol': (60, 179, 113),
    'La': (0, 191, 255),
    'Ti': (132, 112, 255)
}

SOUND_DIR = "C:/Users/LOQ/OneDrive/Documents/maya/2024/scripts/FollowMeGame/sound"
GRAY = (0.5, 0.5, 0.5)

def Create_object():
    clear_scene()
    spacing = 4
    objects = []
    for i, note in enumerate(NOTE_COLORS.keys()):
    	if note == 'Do':
    		obj = cmds.polySphere(name=f'{note}_note')[0]
    	elif note == 'Re':
    		obj = cmds.polyCube(name=f'{note}_note')[0]
    	elif note == 'Mi':
    		obj = cmds.polyCone(name=f'{note}_note')[0]
    	elif note == 'Fa':
    		obj = cmds.polyCylinder(name=f'{note}_note')[0]
    	elif note == 'Sol':
    		obj = cmds.polyTorus(name=f'{note}_note')[0]
    	elif note == 'La':
    		obj = cmds.polyPyramid(name=f'{note}_note')[0]
    	elif note == 'Ti':
    		obj = cmds.polyPlatonicSolid(name=f'{note}_note')[0]

    	cmds.move(i* spacing, 0, 0, obj)
    	set_color(obj, GRAY)
    	objects.append((obj, note))
    return objects

def set_color(obj, rgb):
    shape = cmds.listRelatives(obj, shapes=True)[0]
    shader = cmds.shadingNode('lambert', asShader=True, name=f'{obj}_shader')
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{obj}_SG')
    cmds.connectAttr(f'{shader}.outColor', f'{sg}.surfaceShader', force=True)
    cmds.setAttr(f'{shader}.color', *rgb, type='double3')
    cmds.sets(obj, e=True, forceElement=sg)

def blink_object(obj, note, duration=0.5):
    color = NOTE_COLORS[note]
    shape = cmds.listRelatives(obj, shapes=True)[0]
    shaders = cmds.listConnections(shape, type='lambert')
    if not shaders:
    	return
    shader = shaders[0]
    cmds.setAttr(f'{shader}.color', *color, type='double3')
    cmds.refresh()
    play_note(note)
    time.sleep(duration)
    cmds.setAttr(f'{shader}.color', *GRAY, type='double3')
    cmds.refresh()

def play_note(note):
    path = os.path.join(SOUND_DIR, f'{note}.wav').replace('\\','/')
    if os.path.exists(path):
        mel.eval(f"sound -p 0 -file '{path}';")
    else:
        print(f'Sound file for {note} not found: {path}')

def shuffle_object_positions(objects):
    positions = [cmds.xform(obj[0], q=True, ws=True, t=True) for obj in objects]
    random.shuffle(positions)
    for i, (obj, _) in enumerate(objects):
        cmds.xform(obj, ws=True, t=positions[i])

def clear_scene():
    objs = cmds.ls('*_note')
    if objs:
        cmds.delete(objs)
>>>>>>> 84d13bc (Follow Me)
