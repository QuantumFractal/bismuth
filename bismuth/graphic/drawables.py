

import moderngl as gl

import numpy as np

class BasicTriangle():
    def __init__(self, ctx):
        self.prog = ctx.program(
                vertex_shader='''
                    #version 330
                    in vec2 in_vert;

                    uniform mat4 Mvp;

                    void main() {
                        gl_Position = Mvp * vec4(in_vert, 0.0, 1.0);
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

        self.mvp = self.prog['Mvp']
        vertices = np.array([
            0.0, 0.8,
            -0.6, -0.8,
            0.6, -0.8,
        ])

        self.vbo = ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')
    
    def render(self, mvp):
        self.mvp.write(mvp.astype('f4').tobytes())
        self.vao.render(gl.TRIANGLE_STRIP)
