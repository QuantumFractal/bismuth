'''
    Renders a blue triangle
'''

import numpy as np
from pyrr import Matrix44

import moderngl as gl
import moderngl_window as mglw

from bismuth.graphic import drawables


class HelloWorld(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Hello World"
    window_size = (400, 300)
    aspect_ratio = 4 / 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        # things to draw 
        self.drawables = [drawables.Axes(self.ctx)]



    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


    def render(self, time, frame_time):

        #self.ctx.wireframe = True
        self.ctx.clear(1.0, 1.0, 1.0)


        camX = np.sin(time) * 4
        camY = np.cos(time) * 4
        
        model = Matrix44.identity().from_y_rotation(np.pi * time / 2)
        view = Matrix44.look_at((10.0, 5.0, 10.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 100.0)

        for drawable in self.drawables:
            drawable.render(model, view, projection)


if __name__ == '__main__':
    HelloWorld.run()