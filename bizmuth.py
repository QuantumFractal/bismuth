import ctypes
import cairo
import math
import random

from pyglet import app, clock, gl, image, window
from pyglet.window import key

# create data shared by ImageSurface and Texture
width, height = 1024, 1024

surface_data = (ctypes.c_ubyte * (width * height * 4))()
surface = cairo.ImageSurface.create_for_data (surface_data, cairo.FORMAT_ARGB32,
width, height, width * 4);
texture = image.Texture.create_for_size(gl.GL_TEXTURE_2D, width, height, gl.GL_RGBA)

window = window.Window(width=width, height=height)
ctx = cairo.Context(surface)


center = (width/2, height/2)

counter = 0


MAX_STEPS = 10
#new_child = lambda parent, size, angle: {'parent': parent, 'pos': pos, 'size': size, 'angle': angle, 'child': None}

def new_child(parent, pos, size, angle):
    if parent is not None:
        pos = (parent['pos'][0] + (r * math.cos(cur['angle'])), parentpos[1] + (r * math.sin(cur['angle'])))
        return {'parent': parent, 'pos': pos, }
    else:
        return {'parent': None, 'pos': pos, 'size': size, 'angle': angle, 'child': None}

def grow_tree():
    # parameter
    og = 40
    trunk_size = og
    wiggle = math.radians(90)

    tree = new_child(None, 20, random.uniform(0, math.pi*2))
    cur = tree
    while trunk_size > 0:
        trunk_size -= 1
        angle = random.uniform(cur['angle'] - wiggle *  (1- (trunk_size/og)), cur['angle'] + wiggle * (1- (trunk_size/og)))
        cur['child'] = new_child(cur, 20, angle)
        cur = cur['child']
    return tree

def grow_one_step(root, wiggle, size, step):
    # look for child
    while root['child'] is not None:
        root = root['child']

    root_angle = root['angle']
    root_radius = root['size']
    angle = random.uniform(root_radius - wiggle, root_radius + wiggle)
    root['child'] = new_child(root, size, angle)


def draw_tree(tree, ctx):
    cur = tree
    pos = center
    while cur is not None:
        ctx.arc(*pos, cur['size'], 0, 2*math.pi)
        ctx.set_source_rgb(76/256, 122/256, 112/256)
        ctx.stroke()

        r = cur['size']


        ctx.set_source_rgb(231/256, 156/256, 74/256)
        ctx.move_to(*pos)
        pos = (pos[0] + (r * math.cos(cur['angle'])), pos[1] + (r * math.sin(cur['angle'])))
        ctx.line_to(*pos)
        ctx.stroke()
        cur = cur['child']


def clear_surface(ctx):
    lg1 = cairo.LinearGradient(0.0, 0.0, 350.0, 350.0)
    lg1.add_color_stop_rgba(0, 5/256, 10/256, 24/256, 1)
    lg1.add_color_stop_rgba(1, 24/256, 51/256, 104/256, 1)

    ctx.rectangle(0, 0, width, height)
    ctx.set_source(lg1)
    #ctx.set_source_rgb(4/256, 49/256, 69/256)
    ctx.fill()


forest = []
for x in range(6):
    forest.append(new_child(None, random.randint(5,35), 10, random.uniform(0, math.pi)))
step = 0

def update(dt):
    global step
    if step < MAX_STEPS:
        clear_surface(ctx)
        for tree in forest:
            grow_one_step(tree, math.radians(40), 50, step)
            draw_tree(tree, ctx)
        step += 1

clock.schedule_interval(update, 1/30)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print('The "A" key was pressed.')
    elif symbol == key.LEFT:
        print('The left arrow key was pressed.')
    elif symbol == key.SPACE:
        clear_surface(ctx)
        global forest, step
        step = 0
        forest = []
        for x in range(2):
            forest.append(new_child(None, 20, 0))

@window.event
def on_draw():
    window.clear()

    # Draw texture backed by ImageSurface
    gl.glEnable(gl.GL_TEXTURE_2D)

    gl.glBindTexture(gl.GL_TEXTURE_2D, texture.id)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_BGRA, gl.GL_UNSIGNED_BYTE, surface_data)

    gl.glBegin(gl.GL_QUADS)
    gl.glTexCoord2f(0.0, 1.0)
    gl.glVertex2i(0, 0)
    gl.glTexCoord2f(1.0, 1.0)
    gl.glVertex2i(width, 0)
    gl.glTexCoord2f(1.0, 0.0)
    gl.glVertex2i(width, height)
    gl.glTexCoord2f(0.0, 0.0)
    gl.glVertex2i(0, height)
    gl.glEnd()

# call clock.schedule_update here to update the ImageSurface every frame
app.run()