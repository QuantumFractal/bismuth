

import moderngl as gl
import moderngl_window as glw

import numpy as np

class BasicTriangle():
    def __init__(self, ctx):
        self.prog = ctx.program(
                vertex_shader='''
                    #version 330
                    in vec3 in_vert;

                    uniform mat4 model;
                    uniform mat4 view;
                    uniform mat4 projection;
                    
                    void main() {
                        gl_Position = projection * view * model * vec4(in_vert, 1.0);
                    }
                ''',
                fragment_shader='''
                    #version 330
                    out vec4 f_color;
                    void main() {
                        f_color = vec4(0.0, 0.0, 1.0, 1.0);
                    }
                ''',
            )

        self.model = self.prog['model']
        self.view = self.prog['view']
        self.projection = self.prog['projection']

        t = 1.0
        vertices = np.array([
            t, t, 0.0,
            t, -t, 0.0,
            -t, t, 0.0,
            -t, -t, 0.0,
        ])

        self.vbo = ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')
    
    def render(self, model, view, projection):
        self.model.write(model.astype('f4').tobytes())
        self.view.write(view.astype('f4').tobytes())
        self.projection.write(projection.astype('f4').tobytes())
        self.vao.render(gl.TRIANGLE_STRIP)


class Rect():
    def __init__(self, ctx, window):
        self.prog = ctx.program(
            vertex_shader='''
                #version 330

                in vec3 in_vert;
                in vec2 in_text;

                uniform mat4 model;
                uniform mat4 view;
                uniform mat4 projection;

                out vec3 out_vert;
                out vec2 out_text;

                void main() {
                    gl_Position = projection * view * model * vec4(in_vert, 1.0);
                    out_vert = in_vert;
                    out_text = in_text;
                }
            ''',
            fragment_shader='''
                #version 330

                uniform sampler2D Texture;

                in vec3 in_vert;
                in vec2 out_text;

                out vec4 f_color;
                void main() {
                    float lum = 1.0;
                    f_color = vec4(texture(Texture, out_text).rgb, 1.0);

                }
            ''',
        )

        self.model = self.prog['model']
        self.view = self.prog['view']
        self.projection = self.prog['projection']

        self.Texture = window.load_texture_2d('textures/bricks.png')
        self.obj = window.load_scene('si')

        t = 3.0
        vertices = np.array([
            t, t, 0.0,
            t, -t, 0.0,
            -t, t, 0.0,
            -t, -t, 0.0,
        ])

        v = 100.0
        tx_coords = np.array([
            1.0, 1.0,
            1.0, 0.0,
            0.0, 1.0,
            0.0, 0.0,
        ])

        self.vao = glw.opengl.vao.VAO(name="axes", mode=gl.TRIANGLE_STRIP)
        self.vao.buffer(tx_coords.astype('f4').tobytes(), '2f', ['in_text'])
        self.vao.buffer(vertices.astype('f4').tobytes(), '3f', ['in_vert'])

    def render(self, model, view, projection):

        self.model.write(model.astype('f4').tobytes())
        self.view.write(view.astype('f4').tobytes())
        self.projection.write(projection.astype('f4').tobytes())

        self.Texture.use()
        self.vao.render(self.prog)


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

        t = 0.1
        r = t
        l = 4.0

        vertices = np.array([
            # X Axis
            t, t, r,
            t, -t, r,
            -t, t, r,
            -t, -t, r,
            
            -t, -t, l,
            t, -t, r,
            t, -t, l,
            t, t, r,

            t, t, l,
            -t, t, r,
            -t, t, l,
            -t, -t, r,

            -t, -t, l,
            -t, t, l,
            t, -t, l,
            t, t, r,
            t, t, r,


            # Y Axis
            r, t, t,
            r, t, -t,
            r, -t, t,
            r, -t, -t,

            l, -t, -t,
            r, t, -t,
            l, t, -t,
            r, t, t,

            l, t ,t,
            r, -t, t,
            l, -t, t,
            r, -t, -t,

            l, -t, -t,
            l, -t, t,
            l, t, t,
            r, t, t,
            r, t, t,

            # Z Axis
            t, r, t,
            t, r, -t,
            -t, r, t,
            -t, r, -t,

            -t, l, -t,
            t, r, -t,
            t, l, -t,
            t, r, t,

            t, l, t,
            -t, r, t,
            -t, l, t,
            -t, r, -t,

            -t, l, -t,
            -t, l, t,
            t, l, t,
            t, r, t
        ])

        red = np.tile(np.array([219/255, 126/255, 125/255]), 16)
        green = np.tile(np.array([144/255, 176/255, 141/255]), 17)
        blue = np.tile(np.array([160/255, 224/255, 246/255]), 16)
        colors = np.concatenate((red, green, blue), axis=0)

        self.vbo = ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = glw.opengl.vao.VAO(name="axes", mode=gl.TRIANGLE_STRIP)
        self.vao.buffer(vertices.astype('f4').tobytes(), '3f', ['in_vert'])
        self.vao.buffer(colors.astype('f4').tobytes(), '3f', ['in_color'])

    def render(self, model, view, projection):
        self.model.write(model.astype('f4').tobytes())
        self.view.write(view.astype('f4').tobytes())
        self.projection.write(projection.astype('f4').tobytes())
        self.vao.render(self.prog)



class Grid():
    def __init__(self, ctx, x_lines=5, y_lines=5, thickness=2, border=0.1):
        self.prog = ctx.program(
            vertex_shader='''
                #version 330

                in vec3 in_vert;

                void main() {
                    gl_Position = vec4(in_vert, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                out vec4 f_color;
                void main() {
                    float lum = 1.0;
                    f_color = vec4(1.0, 1.0, 1.0, 1.0);

                }
            ''',
        )

        x_rng = (-1.0, 1.0)
        y_rng = (-1.0, 1.0)

        x_rng = (x_rng[0] + border, x_rng[1] - border)
        y_rng = (y_rng[0] + border, y_rng[1] - border)

        _, _, width, height = ctx.viewport    
        x_thick = thickness/width
        y_thick = thickness/height

        outline = np.array([
            x_rng[0], y_rng[0], 0.0,
            x_rng[1], y_rng[0], 0.0,
            x_rng[1], y_rng[1], 0.0,
            x_rng[0], y_rng[1], 0.0
        ])

        print(outline)
        self.outline = glw.opengl.vao.VAO(mode=gl.LINE_LOOP)
        self.outline.buffer(outline.astype('f4').tobytes(), '3f', ['in_vert'])

        bl = (x_rng[0], y_rng[0])

        grid_lines = []
        v_sep = (x_rng[1] - x_rng[0]) / y_lines
        for x in range(y_lines):
            sep = x * v_sep
            pts = [bl[0] + sep, y_rng[0], 0.0,
                   bl[0] + sep, y_rng[1], 0.0,
                   bl[0] + sep + x_thick, y_rng[1], 0.0,
                   bl[0] + sep + x_thick, y_rng[0], 0.0,
                   bl[0] + sep + x_thick, y_rng[1], 0.0,
                   bl[0] + sep, y_rng[0], 0.0]
            grid_lines += pts

        h_sep = (y_rng[1] - y_rng[0]) / x_lines
        for y in range(x_lines):
            sep = y * h_sep
            pts = [bl[0], bl[1] + sep, 0.0,
                   x_rng[1], bl[1] + sep, 0.0,
                   x_rng[1], bl[1] + sep + y_thick, 0.0,
                   bl[0], bl[1] + sep, 0.0,
                   bl[0], bl[1] + sep + y_thick, 0.0,
                   x_rng[1], bl[1] + sep + y_thick, 0.0]
                   
            grid_lines += pts
    
        grid_lines = np.array(grid_lines)

        self.grid_lines = glw.opengl.vao.VAO(mode=gl.TRIANGLES)
        self.grid_lines.buffer(grid_lines.astype('f4').tobytes(), '3f', ['in_vert'])

    
    def render(self):
        self.outline.render(self.prog)
        self.grid_lines.render(self.prog)
        #self.vao.render(self.prog)

