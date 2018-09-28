import ctypes
import cairo
import math
import random
import queue
import colorsys

import forest
import algae
from pyglet import app, clock, gl, image, window
from pyglet.window import key, mouse


# create data shared by ImageSurface and Texture
width, height = 1024, 1024

surface_data = (ctypes.c_ubyte * (width * height * 4))()
surface = cairo.ImageSurface.create_for_data (surface_data, cairo.FORMAT_ARGB32,
width, height, width * 4);
texture = image.Texture.create_for_size(gl.GL_TEXTURE_2D, width, height, gl.GL_RGBA)

window = window.Window(width=width, height=height)
ctx = cairo.Context(surface)

def get_random_angle():
    return random.uniform(0, math.pi*2)

root_root = None
kd_tree = None
mouse_pos = {'x': 0, 'y': 0}

seed = algae.cell(position=(width / 2, height / 2), size=10)
algae_cluster = algae.cluster(seed, bounds)

usage_state_map = {'SELECT': 'PLACE',
                   'PLACE': 'SELECT'}
usage_mode = 'PLACE'


bounds = forest.boundingBox(20,20, width-20, height-20)




def clear_surface(ctx):
    lg1 = cairo.LinearGradient(0.0, 0.0, 350.0, 350.0)
    lg1.add_color_stop_rgba(0, 5/256, 10/256, 24/256, 1)
    lg1.add_color_stop_rgba(1, 24/256, 51/256, 104/256, 1)

    ctx.rectangle(0, 0, width, height)
    ctx.set_source(lg1)
    #ctx.set_source_rgb(4/256, 49/256, 69/256)
    ctx.fill()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        if usage_mode == 'PLACE':
            global kd_tree
            kd_tree = forest.insert_point(kd_tree, (x, height -y))
            clear_surface(ctx)
            forest.draw_tree(ctx, kd_tree, forest.boundingBox(0, 0, width, height))

@window.event
def on_mouse_motion(x, y, dx, dy):
   mouse_pos['x'] = x
   mouse_pos['y'] = y


def grow_once(dt):


def calc_nearest(dt):
    if usage_mode == 'SELECT':
        x = mouse_pos['x']
        y = mouse_pos['y']

        clear_surface(ctx)
        #print('-'*10)
        #print(f"Query Point: ({x}, {height - y})")
        ctx.save()
        ctx.set_source_rgb(1,0,1)
        ctx.arc(x, height - y, 5, 0, math.pi * 2)
        ctx.fill()
        ctx.restore()
        
        #point = forest.betterNearestNeighbor((x, height - y), kd_tree, None)
        point = forest.bestNN((x, height - y), kd_tree) #None, math.inf, forest.boundingBox(0, 0, width, height))
        forest.draw_tree(ctx, kd_tree, forest.boundingBox(0, 0, width, height))

        if point is not None:      
            dist = forest.distance((x, height - y), point.point)
            #print(f">>>> Point: {str(point)}, Dist: {dist}")         
            ctx.save()
            ctx.set_source_rgb(1,1,1)
            ctx.arc(*point.point, dist, 0, math.pi * 2)
            ctx.stroke()
            ctx.restore()
        else:
            pass
            #print('>>>> None found')

@window.event
def on_key_press(symbol, modifiers):
    global kd_tree
    if symbol == key.A:
        print('-'*10)
        forest.print_tree(kd_tree)

    elif symbol == key.LEFT:
        clear_surface(ctx)
        root_root.grow_once()
        root_root.draw(ctx)

    elif symbol == key.T:
        global usage_mode
        usage_mode = usage_state_map[usage_mode]
        print(f"Usage mode : {usage_mode}")

    elif symbol == key.SPACE:
        clear_surface(ctx)
        algae_cluster.reset()


@window.event
def on_draw():
    window.clear()
    root_root.draw(ctx)
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
    root_root = root()
    #clock.schedule_interval(calc_nearest, 1/30)
    clock.schedule_interval(grow_once, 1/5)
    clear_surface(ctx)

    #forest.draw_tree(ctx, root_root.kd, world)

    #forest.draw_tree(ctx, kd, (0, width), width, height)
    #Fforest.print_tree(root_root.kd)

    # call clock.schedule_update here to update the ImageSurface every frame
    app.run()