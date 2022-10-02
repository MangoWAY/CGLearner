from base import shader, window_helper
from OpenGL import GL as gl
from base.gl_render_data import *
import glfw

window_config = window_helper.Window.Config(bgcolor = (0.5,0.5,0.5))
window = window_helper.Window(window_config)
mshader = shader.Shader()
mshader.load_shader_source_from_path(shader.ShaderType.VERTEX, "shader/base.vert")
mshader.load_shader_source_from_path(shader.ShaderType.FRAGMENT, "shader/base.frag")
mshader.create_program()
mshader.use_program()

data = RendererData()
desp = VertexAttribDesp()
desp.attr_id = 0
desp.comp_count = 3
desp.stride = 3 * 4
desp.offset = None
desp.need_nor = False
desp.comp_type = gl.GL_FLOAT

vert = [-0.5, 0.5, 0,
        0.5, 0.5, 0,
        0.5, -0.5, 0,
        -0.5, -0.5 ,0 ]
inde = [
    3,1,0,
    3,2,1
]

data.build_data([desp],vert,inde)
data.use()

while (
        glfw.get_key(window.native_window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window.native_window)
    ):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        data.draw()
        glfw.swap_buffers(window.native_window)
        glfw.poll_events()