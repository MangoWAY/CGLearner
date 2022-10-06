import random
from base import shader, window_helper, transform
from OpenGL import GL as gl
from base.camera import Camera
from base.gl_render_data import *
from base.model_importer import *
import glfw

from base.texture import Texture

window_config = window_helper.Window.Config(bgcolor = (0.5,0.5,0.5))
window = window_helper.Window(window_config)
mshader = shader.Shader()
mshader.load_shader_source_from_path(shader.ShaderType.VERTEX, "shader/base.vert")
mshader.load_shader_source_from_path(shader.ShaderType.FRAGMENT, "shader/base.frag")
mshader.create_program()
mshader.use_program()

trans = transform.Transform()
trans.localPosition = [0,2,0]
trans.localScale = [10,10,10]
trans.localEulerAngle = [-90,45,0]
model = trans.localMatrix()

viewTrans = transform.Transform()
viewTrans.localPosition = [0,3,20]
viewTrans.localEulerAngle = [0,0,0]
view = viewTrans.get_to_Local()

cam = Camera()
proj = cam.getProjectionMatrix()

mvp = np.transpose(proj @ view @ model)
mshader.set_mat4("u_mvp", mvp)


desp = VertexAttribDesp()
desp.attr_id = 0
desp.comp_count = 3
desp.stride = 11 * 4
desp.offset = ctypes.c_void_p(0)
desp.need_nor = False
desp.comp_type = gl.GL_FLOAT

desp1 = VertexAttribDesp()
desp1.attr_id = 1
desp1.comp_count = 3
desp1.stride = 11 * 4
desp1.offset = ctypes.c_void_p(12)
desp1.need_nor = False
desp1.comp_type = gl.GL_FLOAT

desp2 = VertexAttribDesp()
desp2.attr_id = 2
desp2.comp_count = 3
desp2.stride = 11 * 4
desp2.offset = ctypes.c_void_p(24)
desp2.need_nor = False
desp2.comp_type = gl.GL_FLOAT

desp3 = VertexAttribDesp()
desp3.attr_id = 3
desp3.comp_count = 2
desp3.stride = 11 * 4
desp3.offset = ctypes.c_void_p(36)
desp3.need_nor = False
desp3.comp_type = gl.GL_FLOAT

importer = ModelImporter()

meshes = importer.load_mesh("1.fbx")
verts = []
indes = []
renderData = []
for mesh in meshes:
    vert = []
    for i in range(len(mesh.vertices)):
        if i % 3 == 0:
            vert.extend([mesh.vertices[i],mesh.vertices[i + 1],mesh.vertices[i + 2]])
            vert.extend([mesh.normals[i],mesh.normals[i + 1],mesh.normals[i + 2]])
            vert.extend([random.random(),random.random(),random.random()])
            vert.extend([mesh.uvs[int(i/3),0],mesh.uvs[int(i/3),1]])
    verts.append(vert)
    inde = mesh.subMeshes[0].indices
    indes.append(inde)
    data = RendererData()
    data.build_data([desp,desp1,desp2,desp3],vert, inde)
    renderData.append(data)
gl.glEnable(gl.GL_DEPTH_TEST)

tex = Texture()
tex.create()
tex.load_from_path("default_Base_Color.png")
tex.bind()

while (
        glfw.get_key(window.native_window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window.native_window)
    ):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        for data in renderData:
            data.use()
            data.draw()
            data.unuse()
        glfw.swap_buffers(window.native_window)
        glfw.poll_events()