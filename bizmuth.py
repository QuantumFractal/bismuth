import ctypes
import cairo
import math
import random
import queue

import forest
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

def get_random_angle():
    return random.uniform(0, math.pi*2)

root_root = None


class cap:
    def __init__(self, parent=None, size=10, direction=math.pi, pos=(0,0), children=[]):
        self.parent = parent
        self.size = size
        self.direction = direction
        self.pos = pos
        self.children = children

    def __str__(self):
        return f"""<{','.join(str(x) for x in self.pos)}>"""


class root(cap):
    def __init__(self):
        super().__init__(parent=None, pos=(width/2, height/2), size=30, direction=random.uniform(0, math.pi*2), children=[])
        self.leaves = set()
        self.leaves.add(self)
        self.kd = forest.kdNode(self.pos)


    def reset(self):
        self.children.clear()
        self.leaves.clear()
        self.leaves.add(self)

    def grow(self):
        leaf = random.sample(self.leaves, 1)[0]
        self.leaves.remove(leaf)
        
        # caluclate new pos
        direction = random.uniform(0, math.pi*2)
        size = 50
        pos = (leaf.size * math.cos(direction) + leaf.pos[0], leaf.size * math.sin(direction) + leaf.pos[1])
        new_cap = cap(parent=leaf, pos=pos, direction=direction, size=size)
        self.kd = forest.insert_point(self.kd, pos)
        self.leaves.add(new_cap)
        self.children.append(new_cap)

    def draw(self, ctx):
        q = queue.Queue()

        q.put(self)
        while not q.empty():
            cur = q.get()

            if cur in self.leaves:
                ctx.set_source_rgb(1, .5, .5)
            else:
                ctx.set_source_rgb(1,1,1)
            ctx.arc(*cur.pos, cur.size, 0, math.pi*2)
            ctx.fill()


            for child in cur.children:
                q.put(child)


def clear_surface(ctx):
    lg1 = cairo.LinearGradient(0.0, 0.0, 350.0, 350.0)
    lg1.add_color_stop_rgba(0, 5/256, 10/256, 24/256, 1)
    lg1.add_color_stop_rgba(1, 24/256, 51/256, 104/256, 1)

    ctx.rectangle(0, 0, width, height)
    ctx.set_source(lg1)
    #ctx.set_source_rgb(4/256, 49/256, 69/256)
    ctx.fill()


def update(dt):
    pass


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print('The "A" key was pressed.')
    elif symbol == key.LEFT:
        print('The left arrow key was pressed.')
    elif symbol == key.SPACE:
        clear_surface(ctx)
        root_root.reset()
        for x in range(100):
            root_root.grow()
        root_root.draw(ctx)
        forest.print_tree(root_root.kd)


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
    clock.schedule_interval(update, 1/30)
    clear_surface(ctx)
    root_root = root()
    for x in range(5):
        root_root.grow()
    root_root.draw(ctx)

    forest.print_tree(root_root.kd)
    forest.draw_tree(ctx, root_root.kd, (0, width), width, height)

    # call clock.schedule_update here to update the ImageSurface every frame
    app.run()