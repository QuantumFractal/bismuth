'''
    Renders a blue triangle
'''

import numpy as np
import os
from pyrr import Matrix44

import moderngl as gl
import moderngl_window as mglw

from bismuth.graphic import drawables


class Plotter(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Plotter V1"
    window_size = (400, 300)
    aspect_ratio = 4 / 3
    samples = 0
    resource_dir = os.path.normpath(os.path.join(__file__, ".."))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # things to draw 
        #drawables.Axes(self.ctx), 
        self.drawables = [drawables.Grid(self.ctx, x_lines=7, y_lines=7, thickness=4)]


    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


    def render(self, time, frame_time):

        self.ctx.clear(0.1, 0.1, 0.1) 
        self.ctx.enable(gl.BLEND)
        self.ctx.enable(gl.DEPTH_TEST)

        for drawable in self.drawables:
            drawable.render()


if __name__ == '__main__':
    Plotter.run()