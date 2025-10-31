import maya.cmds as cmds
import random
import time
import os
import maya.mel as mel

NOTE_COLORS = {
    'Do': (255, 0, 0),
    'Re': (255, 144, 0),
    'Mi': (255, 215, 0),
    'Fa': (0, 255, 0),
    'Sol': (32, 178, 170),
    'La': (0, 191, 255),
    'Ti': (132, 112, 255)
}

SOUND_DIR = "C:/Users/LOQ/OneDrive/Documents/maya/2024/scripts/FollowMeGame/sound"
print("exists:", os.path.exists(SOUND_DIR))
try:
    import winsound
    winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    print("winsound called")
except Exception as e:
    print("winsound failed:", e)
try:
    import os
    os.startfile(path)
    print("os.startfile called")
except Exception as e:
    print("os.startfile failed:", e)

GRAY = (139, 137, 137)

def create_object():
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
    align_objects_to_grid(objects)
    return objects

def set_color(obj, rgb, brightness=0.7):
    shape = cmds.listRelatives(obj, shapes=True)[0]
    shader_name = f"{obj}_shader"
    sg_name = f"{obj}_SG"

    if cmds.objExists(shader_name):
        cmds.delete(shader_name)
    if cmds.objExists(sg_name):
        cmds.delete(sg_name)

    shader = cmds.shadingNode('lambert', asShader=True, name=shader_name)
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_name)

    cmds.connectAttr(f'{shader}.outColor', f'{sg}.surfaceShader', force=True)
    scaled_rgb = [brightness * (c / 255.0) for c in rgb]  # ปรับลดความสว่าง
    cmds.setAttr(f'{shader}.color', *scaled_rgb, type='double3')
    cmds.sets(obj, e=True, forceElement=sg)
    cmds.refresh(f=True)

def shuffle_object_positions(objects):
    random.shuffle(objects)
    for i, (obj, _) in enumerate(objects):
        cmds.move(i * 3, 0, 0, obj)
    cmds.refresh(f=True)

def play_note(note):
    path = os.path.join(SOUND_DIR, f'{note}.wav').replace('\\', '/')
    if not os.path.exists(path):
        print(f'[FollowMe util] Sound file for {note} not found: {path}')
        return
    try:
        import winsound
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        print(f'[FollowMe util] Playing (winsound) {path}')
        return
    except Exception as e:
        print(f'[FollowMe util] winsound failed: {e}')

    try:
        if os.name == 'nt':
            os.startfile(path)
            print(f'[FollowMe util] Playing (os.startfile) {path}')
            return
    except Exception as e:
        print(f'[FollowMe util] os.startfile failed: {e}')

    try:
        import subprocess
        subprocess.Popen(['start', path], shell=True)
        print(f'[FollowMe util] Playing (subprocess start) {path}')
        return
    except Exception as e:
        print(f'[FollowMe util] subprocess start failed: {e}')

    try:
        node = cmds.sound(file=path)
        print(f'[FollowMe util] Created Maya sound node: {node} (may require manual play)')
        return
    except Exception as e:
        print(f'[FollowMe util] cmds.sound failed: {e}')

    print('[FollowMe util] All playback methods failed.')


def clear_scene():
    notes = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Ti']

    for note in notes:
        objs = cmds.ls(f'{note}_note*', dag=True, long=True) or []
        objs += cmds.ls(f'{note}_Note*', dag=True, long=True) or []

        for obj in objs:
            shader = f"{obj}_shader"
            sg = f"{obj}_SG"
            if cmds.objExists(shader):
                cmds.delete(shader)
            if cmds.objExists(sg):
                cmds.delete(sg)
            if cmds.objExists(obj):
                try:
                    cmds.delete(obj)
                except:
                    pass

    for node_type in ['shadingEngine', 'lambert', 'surfaceShader']:
        all_nodes = cmds.ls(type=node_type)
        for node in all_nodes:
            if node.endswith('_SG') or node.endswith('_shader'):
                try:
                    cmds.delete(node)
                except:
                    pass

    cmds.refresh(f=True)

def align_objects_to_grid(objects):
    for obj, _ in objects:
        if not cmds.objExists(obj):
            continue
        bbox = cmds.exactWorldBoundingBox(obj)
        minY = bbox[1]
        cmds.move(0, -minY, 0, obj, relative=True)

