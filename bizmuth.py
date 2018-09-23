import ctypes
import cairo
import math
import random
import queue
import colorsys

import forest
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
world = forest.boundingBox(20,20, width-20, height-20)

class cap:
    def __init__(self, parent=None, size=10, direction=math.pi, pos=(0,0), children=[]):
        self.parent = parent
        self.size = size
        self.direction = direction
        self.pos = pos
        self.children = children

    def __str__(self):
        return f"""<{','.join(str(x) for x in self.pos)}>"""



def inverse_square(x):
    return (1 / (4*math.pi*(x + (1/(2*math.sqrt(math.pi)))**2)))


class root(cap):
    def __init__(self):
        super().__init__(parent=None, pos=(width/2, height/2), size=40, direction=random.uniform(0, math.pi*2), children=[])
        self.leaves = set()
        self.leaves.add(self)
        self.kd = forest.kdNode(self.pos)
        self.depth = 40
        self.max_depth = 40


    def reset(self):
        self.children.clear()
        self.leaves.clear()
        self.leaves.add(self)
        self.kd = forest.kdNode(self.pos)
        self.depth = self.max_depth
        self.direction = random.uniform(0, math.pi*2)

    def grow(self):
        while self.depth > 5:
            self.grow_once()
            self.depth -= 1

    def grow_once(self):
        leaf = random.sample(self.leaves, 1)[0]
        self.leaves.remove(leaf)
        
        # caluclate new pos
        wiggle = math.radians(30)
        direction = random.uniform(leaf.direction - wiggle, leaf.direction + wiggle)
        size = inverse_square(1-(self.depth / self.max_depth)) * self.max_depth
        print(size)
        pos = (leaf.size * math.cos(direction) + leaf.pos[0], leaf.size * math.sin(direction) + leaf.pos[1])
        if pos in world:
            new_cap = cap(parent=leaf, pos=pos, direction=direction, size=size)
            self.kd = forest.insert_point(self.kd, pos)
            self.leaves.add(new_cap)
            self.children.append(new_cap)
        else: # DEATH!!!
            self.depth = 0

    def draw(self, ctx):
        q = queue.Queue()
        q.put(self)
        while not q.empty():
            cur = q.get()

            if cur in self.leaves:
                ctx.set_source_rgb(1, 0, 0)
            else:
                color = colorsys.hsv_to_rgb(0.3, .75, .75)
                ctx.set_source_rgba(*color, 0.5)
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
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        pass
        global kd_tree
        kd_tree = forest.insert_point(kd_tree, (x, height-y))
        clear_surface(ctx)
        forest.draw_tree(ctx, kd_tree, world)

@window.event
def on_key_press(symbol, modifiers):
    global kd_tree
    if symbol == key.A:
        forest.print_tree(kd_tree)
    elif symbol == key.LEFT:
        clear_surface(ctx)
        root_root.grow_once()
        root_root.draw(ctx)

    elif symbol == key.SPACE:
        clear_surface(ctx)
        root_root.reset()
        root_root.grow()
        root_root.draw(ctx)
        #forest.draw_tree(ctx, root_root.kd,  bb=world)


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
    root_root.grow()
    root_root.draw(ctx)

    #forest.draw_tree(ctx, root_root.kd, world)

    #forest.draw_tree(ctx, kd, (0, width), width, height)
    #Fforest.print_tree(root_root.kd)


    # call clock.schedule_update here to update the ImageSurface every frame
    app.run()