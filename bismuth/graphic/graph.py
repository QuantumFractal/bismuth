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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        # things to draw 
        self.drawables = [drawables.BasicTriangle(self.ctx)]



    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


    def render(self, time, frame_time):

        self.ctx.wireframe = True
        self.ctx.clear(0.1, 0.1, 0.1)


        angle = 0
        proj = Matrix44.perspective_projection(45.0, 400/300, 0.0, 100.0)
        lookat = Matrix44.look_at((np.cos(angle), np.sin(angle), 0.8),
            (0.0, 0.0, 0.1),
            (0.0, 0.0, 1.0),
        )

       
        mvp = proj * lookat
        for drawable in self.drawables:
            drawable.render(mvp)


if __name__ == '__main__':
    HelloWorld.run()