

import moderngl as gl
import moderngl_window as glw

import numpy as np

class BasicTriangle():
    def __init__(self, ctx):
        self.prog = ctx.program(
                vertex_shader='''
                    #version 330
                    in vec2 in_vert;

                    uniform mat4 model;
                    uniform mat4 view;
                    uniform mat4 projection;
                    
                    void main() {
                        gl_Position = projection * view * model * vec4(in_vert, 0.0, 1.0);
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

        self.model = self.prog['model']
        self.view = self.prog['view']
        self.projection = self.prog['projection']

        vertices = np.array([
            0.0, 0.8,
            -0.6, -0.8,
            0.6, -0.8,
        ])

        self.vbo = ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')
    
    def render(self, model, view, projection):
        self.model.write(model.astype('f4').tobytes())
        self.view.write(view.astype('f4').tobytes())
        self.projection.write(projection.astype('f4').tobytes())
        self.vao.render(gl.TRIANGLE_STRIP)


class Axes():
    def __init__(self, ctx):
        self.prog = ctx.program(
                vertex_shader='''
                    #version 330
                    in vec3 in_vert;
                    in vec3 in_color;

                    out vec3 v_color;

                    uniform mat4 model;
                    uniform mat4 view;
                    uniform mat4 projection;
                    
                    void main() {
                        gl_Position = projection * view * model * vec4(in_vert, 1.0);
                        v_color = in_color;
                    }
                ''',
                fragment_shader='''
                    #version 330
                    in vec3 v_color;
                    out vec4 f_color;
                    void main() {
                        f_color = vec4(v_color, 1.0);
                    }
                ''',
            )

        ctx.line_width = 10.0
        self.model = self.prog['model']
        self.view = self.prog['view']
        self.projection = self.prog['projection']

        t = 0.2
        l = 4.0

        vertices = np.array([
            t, t, 0.0,
            t, -t, 0.0,
            -t, t, 0.0,
            -t, -t, 0.0,
            
            -t, -t, l,
            t, -t, 0.0,
            t, -t, l,
            t, t, 0.0,

            t, t, l,
            -t, t, 0.0,
            -t, t, l,

            -t, -t, 0.0,
            -t, -t, l,
            -t, t, l,
            t, -t, l,
            t, t, l
        ])

        colors = np.tile(np.array([1.0, 0.0, 0.0]), len(vertices))

        self.vbo = ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = glw.opengl.vao.VAO(name="axes", mode=gl.TRIANGLE_STRIP)
        self.vao.buffer(vertices.astype('f4').tobytes(), '3f', ['in_vert'])
        self.vao.buffer(colors.astype('f4').tobytes(), '3f', ['in_color'])

    def render(self, model, view, projection):
        self.model.write(model.astype('f4').tobytes())
        self.view.write(view.astype('f4').tobytes())
        self.projection.write(projection.astype('f4').tobytes())
        self.vao.render(self.prog)