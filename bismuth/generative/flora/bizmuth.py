import ctypes
import cairo
import math
import random
import queue
import colorsys

import forest
import algae
import roots
from pyglet import app, clock, gl, image, window
from pyglet.window import key, mouse


# create data shared by ImageSurface and Texture
width, height =  1200, 800

surface_data = (ctypes.c_ubyte * (width * height * 4))()
surface = cairo.ImageSurface.create_for_data (surface_data, cairo.FORMAT_ARGB32,
width, height, width * 4);
texture = image.Texture.create_for_size(gl.GL_TEXTURE_2D, width, height, gl.GL_RGBA)

window = window.Window(width=width, height=height)
ctx = cairo.Context(surface)
ctx.set_antialias(cairo.ANTIALIAS_NONE)
ctx.set_source_rgb(1,1,1)
ctx.arc(500, 500, 50, 0, 7)
ctx.stroke()

def get_random_angle():
    return random.uniform(0, math.pi*2)


mouse_pos = {'x': 0, 'y': 0}

bounds = forest.boundingBox(20,20, width-20, height-20)
kd_tree = forest.kdTree(bounds)

# seed = algae.Cell(position=(width / 2, height / 2))
# algae_cluster = algae.Cluster(seed, bounds)
MULTI_ROOT = True

GLOBAL_KD_TREE = kd_tree

if MULTI_ROOT:
    border = 50
    all_roots = []
    root_size = 30

    # top left
    seed = roots.Cell(position=(border, border), direction=math.radians(45), size=root_size)
    all_roots.append(roots.Roots(seed, None, kd=GLOBAL_KD_TREE, color=(0/256, 120/256, 120/256)))

    # top right
    seed = roots.Cell(position=(width - border, border), direction=math.radians(45 + 90), size=root_size)
    all_roots.append(roots.Roots(seed, None, kd=GLOBAL_KD_TREE, color=(128/256, 128/256, 255/256)))

    # bottom left
    seed = roots.Cell(position=(border, height - border), direction=math.radians(-45), size=root_size)
    all_roots.append(roots.Roots(seed, None, kd=GLOBAL_KD_TREE, color=(200/256, 190/256, 80/256)))

    # bottom right
    seed = roots.Cell(position=(width - border, height - border), direction=math.radians(-45 - 90), size=root_size)
    all_roots.append(roots.Roots(seed, None, kd=GLOBAL_KD_TREE))
else:
    all_roots = []
    seed = roots.Cell(position=(150, 150), direction=math.radians(45), size=30)
    all_roots.append(roots.Roots(seed, forest.boundingBox(20, 20, width - 20, height - 20)))

usage_state_map = {'SELECT': 'PLACE', 'PLACE': 'DELETE', 'DELETE': 'SELECT'}
usage_mode = 'PLACE'


def grow_once(dt):

    for iters in range(10):
        for root in all_roots:
            if root.can_grow():    
                root.grow_once(ctx=ctx)
            else: 
                print("DONE")

    #algae_cluster.grow_cell()
    #algae_cluster.draw(ctx)

def draw(dt):
    clear_surface(ctx)
    for root in all_roots:
        root.draw(ctx)        

def clear_surface(ctx):
    lg1 = cairo.LinearGradient(0.0, 0.0, 0.0, 700.0)
    lg1.add_color_stop_rgba(0, 106/256, 87/256, 68/256, 1)
    lg1.add_color_stop_rgba(1, 74/256, 61/256, 47/256, 1)

    ctx.rectangle(0, 0, width, height)
    ctx.set_source(lg1)
    #ctx.set_source_rgb(4/256, 49/256, 69/256)
    ctx.fill()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        mouse_pos['x'] = x
        mouse_pos['y'] = y

        #root_bundle.grow_once(position= (x, height - y))

        if usage_mode == 'PLACE':
            kd_tree.insert((x, height - y))
            clear_surface(ctx)
            kd_tree.draw(ctx)

        elif usage_mode == 'DELETE':
            clear_surface(ctx)
            pt = kd_tree.nearestNeighbor((x, height - y))
            print(pt)
            if pt is not None:
                kd_tree.delete(pt.point)
            kd_tree.draw(ctx)

        elif usage_mode == 'SELECT':
            clear_surface(ctx)
            kd_tree.draw(ctx)
            pt = kd_tree.nearestNeighbor((x, height - y))
            print(pt)
            ctx.save()
            ctx.set_source_rgb(1,1,1)
            ctx.arc(*pt.point, 20, 0, 7)
            ctx.stroke()
            ctx.restore()


@window.event
def on_key_press(symbol, modifiers):

    if symbol == key.T:
        global usage_mode
        usage_mode = usage_state_map[usage_mode]
        print(f"Usage mode : {usage_mode}")

    if symbol == key.B:
        #grow_once(1)
        node = kd_tree.findMin()
        ctx.set_source_rgb(1,1,1)
        ctx.arc(*node.point, 40, 0, 7)
        ctx.stroke()
        forest.print_tree(kd_tree.root)

    elif symbol == key.SPACE:
        clear_surface(ctx)
        for root in all_roots:
            root.reset()


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


if __name__ == "__main__":
    clock.schedule_interval(draw, 1/60)
    clock.schedule_interval(grow_once, 1/100)
    clear_surface(ctx)
    # root_bundle.grow_once()
    # root_bundle.draw(ctx)

    app.run()