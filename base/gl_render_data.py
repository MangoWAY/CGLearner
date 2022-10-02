from OpenGL import GL as gl
import logging, ctypes
log = logging.getLogger(__name__)
class RendererData:
    def __init__(self) -> None:
        self.vao: VAO = None
        self.vbo: VBO = None
        self.ebo: VBO = None

    def use(self):
        self.vao.bind()

    def unuse(self):
        self.vao.unbind()

    def draw(self):
        self.use()
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.ebo.indices), gl.GL_UNSIGNED_INT, None)
        self.unuse()

    def build_data(self, desp:list, vertices:list, indices:list):
        # create vertex array object
        self.vao = VAO()
        self.vao.create_vertex_array_object()
        self.vao.bind()

        # create vertex buffer object
        self.vbo = VBO()
        self.vbo.vertex_attrib_desps = desp
        self.vbo.vertex_data = vertices
        self.vbo.create_vertex_array_object()
        self.vbo.bind()
        self.vbo.gen_buffer_data()

        # create element buffer object
        self.ebo = EBO()
        self.ebo.indices = indices
        self.ebo.create_index_array_object()
        self.ebo.bind()
        self.ebo.gen_buffer_data()

        # unbind all
        self.vao.unbind()
        self.vbo.unbind()
        self.ebo.unbind()

    def clean(self):
        self.vao.clean()
        self.vbo.clean()
        self.ebo.clean()
        

class VAO:
    def __init__(self) -> None:
        self.vao_id = -1
    
    def clean(self):
        log.debug('cleaning up vertex array')
        gl.glDeleteVertexArrays(1, [self.vao_id])

    def create_vertex_array_object(self):
        log.debug('creating and binding the vertex array (VAO)')
        self.vao_id = gl.glGenVertexArrays(1)

    def bind(self):
        gl.glBindVertexArray(self.vao_id)

    def unbind(self):
        gl.glBindVertexArray(0)
        

class VertexAttribDesp:
    def __init__(self) -> None:
        self.attr_id = 0
        self.comp_count = 3
        self.comp_type = gl.GL_FLOAT
        self.need_nor = False
        self.stride = 0
        self.offset = 0

class EBO:
    def __init__(self) -> None:
        self.indices = []
        self.buffer_id = -1

    def create_index_array_object(self):
        self.buffer_id = gl.glGenBuffers(1)

    def bind(self):
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.buffer_id)

    def unbind(self):
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

    def gen_buffer_data(self):
        array_type = (gl.GLuint * len(self.indices))
        
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, 
                        len(self.indices) * ctypes.sizeof(ctypes.c_uint),
                        array_type(*self.indices),
                        gl.GL_STATIC_DRAW
                        )
    def clean(self):
        log.debug('cleaning up buffer')
        gl.glDeleteBuffers(1, [self.buffer_id])

class VBO:
    def __init__(self) -> None:
        self.vertex_data = [-1, -1, 0,
                        1, -1, 0,
                        0,  1, 0]
        self.vertex_attrib_desps = []
        self.buffer_id = -1
    
    def clean(self):
        log.debug('cleaning up buffer')
        for desp in self.vertex_attrib_desps:
            gl.glDisableVertexAttribArray(desp.attr_id)
        gl.glDeleteBuffers(1, [self.buffer_id])

    def create_vertex_array_object(self):
        self.buffer_id = gl.glGenBuffers(1)

    def bind(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer_id)

    def unbind(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def gen_buffer_data(self):
        array_type = (gl.GLfloat * len(self.vertex_data))
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        len(self.vertex_data) * ctypes.sizeof(ctypes.c_float),
                        array_type(*self.vertex_data),
                        gl.GL_STATIC_DRAW)

        log.debug('setting the vertex attributes')
        for desp in self.vertex_attrib_desps:
            gl.glVertexAttribPointer(
                desp.attr_id,       # attribute 0.
                desp.comp_count,    # components per vertex attribute
                desp.comp_type,     # type
                desp.need_nor,      # to be normalized?
                desp.stride,        # stride
                desp.offset         # array buffer offset
            )
            gl.glEnableVertexAttribArray(desp.attr_id)  # use currently bound VAO