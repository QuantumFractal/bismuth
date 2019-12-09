'''
    Renders a blue triangle
'''

import numpy as np

import moderngl_window as mglw


class HelloWorld(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Hello World"
    window_size = (400, 300)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 in_vert;
                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                out vec4 f_color;
                void main() {
                    f_color = vec4(0.3, 0.5, 1.0, 1.0);
                }
            ''',
        )

        vertices = np.array([
            0.0, 0.8,
            -0.6, -0.8,
            0.6, -0.8,
        ])

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.vao.render()


if __name__ == '__main__':
    HelloWorld.run()