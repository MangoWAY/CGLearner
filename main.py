import random
from base import shader, window_helper, transform
from OpenGL import GL as gl
from base.camera import Camera
from base.gl_render_data import *
from base.model_importer import *
import glfw

window_config = window_helper.Window.Config(bgcolor = (0.5,0.5,0.5))
window = window_helper.Window(window_config)
mshader = shader.Shader()
mshader.load_shader_source_from_path(shader.ShaderType.VERTEX, "shader/base.vert")
mshader.load_shader_source_from_path(shader.ShaderType.FRAGMENT, "shader/base.frag")
mshader.create_program()
mshader.use_program()

trans = transform.Transform()
trans.localPosition = [0,0,0]
trans.localScale = [1,1,1]
trans.localEulerAngle = [0,10,0]
model = trans.localMatrix()

viewTrans = transform.Transform()
viewTrans.localPosition = [0,2,2]
viewTrans.localEulerAngle = [-40,0,0]
view = viewTrans.get_to_Local()

cam = Camera()
proj = cam.getProjectionMatrix()

mvp = np.transpose(proj @ view @ model)
mshader.set_mat4("u_mvp", mvp)

data = RendererData()
desp = VertexAttribDesp()
desp.attr_id = 0
desp.comp_count = 3
desp.stride = 9 * 4
desp.offset = ctypes.c_void_p(0)
desp.need_nor = False
desp.comp_type = gl.GL_FLOAT

desp1 = VertexAttribDesp()
desp1.attr_id = 1
desp1.comp_count = 3
desp1.stride = 9 * 4
desp1.offset = ctypes.c_void_p(12)
desp1.need_nor = False
desp1.comp_type = gl.GL_FLOAT

desp1 = VertexAttribDesp()
desp1.attr_id = 2
desp1.comp_count = 3
desp1.stride = 9 * 4
desp1.offset = ctypes.c_void_p(24)
desp1.need_nor = False
desp1.comp_type = gl.GL_FLOAT

importer = ModelImporter()

meshes = importer.load_mesh("box.fbx")
vert = []
for i in range(len(meshes[0].vertices)):
    if i % 3 == 0:
        vert.extend([meshes[0].vertices[i],meshes[0].vertices[i + 1],meshes[0].vertices[i + 2]])
        vert.extend([meshes[0].normals[i],meshes[0].normals[i + 1],meshes[0].normals[i + 2]])
        vert.extend([random.random(),random.random(),random.random()])
inde = meshes[0].subMeshes[0].indices

data.build_data([desp,desp1],vert,inde)
data.use()
gl.glEnable(gl.GL_DEPTH_TEST)

while (
        glfw.get_key(window.native_window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window.native_window)
    ):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        data.draw()
        glfw.swap_buffers(window.native_window)
        glfw.poll_events()