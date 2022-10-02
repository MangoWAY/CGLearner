import sys
from OpenGL import GL as gl
from enum import Enum
import logging
log = logging.getLogger(__name__)

class ShaderType(Enum):
    VERTEX = 0
    FRAGMENT = 1

class Shader:
    def __init__(self) -> None:
        self.vertex_shader = ""
        self.fragment_shader = ""
        self.program_id = -1
        self.shader_ids = []

    def load_shader_source_from_string(self, shader_type: ShaderType, source: str):
        if shader_type == ShaderType.VERTEX:
            self.vertex_shader = source
        elif shader_type == ShaderType.FRAGMENT:
            self.fragment_shader = source
        else:
            logging.error("wrong shader type !")

    def load_shader_source_from_path(self, shader_type: ShaderType, path: str):
        with open(path,"r") as f:
            source = f.read()
            self.load_shader_source_from_string(shader_type, source)

    def log_shader_info(self, shader_id):
        result = gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS)
        log.debug(f"gl.GL_COMPILE_STATUS {result}")
        info_log_len = gl.glGetShaderiv(shader_id, gl.GL_INFO_LOG_LENGTH)
        if info_log_len:
            logmsg = gl.glGetShaderInfoLog(shader_id)
            log.error(logmsg)
            sys.exit(10)

    def log_program_info(self,program_id):
        # check if linking was successful
        result = gl.glGetProgramiv(program_id, gl.GL_LINK_STATUS)
        log.debug(f"gl.GL_LINK_STATUS {result}")
        info_log_len = gl.glGetProgramiv(program_id, gl.GL_INFO_LOG_LENGTH)
        if info_log_len:
            logmsg = gl.glGetProgramInfoLog(program_id)
            log.error(logmsg)
            sys.exit(11)

    def create_program(self):
        self.program_id = gl.glCreateProgram()
        for shader_type in [gl.GL_VERTEX_SHADER, gl.GL_FRAGMENT_SHADER]:
            shader_id = gl.glCreateShader(shader_type)
            if shader_type == gl.GL_VERTEX_SHADER:
                gl.glShaderSource(shader_id, self.vertex_shader)
            else:
                gl.glShaderSource(shader_id, self.fragment_shader)
            log.debug(f'compiling the {shader_type} shader')
            gl.glCompileShader(shader_id)

            self.log_shader_info(shader_id)

            gl.glAttachShader(self.program_id, shader_id)
            self.shader_ids.append(shader_id)
        log.debug('linking shader program')
        gl.glLinkProgram(self.program_id)

        self.log_program_info(self.program_id)
        log.debug('installing shader program into rendering state')

    def use_program(self):
        gl.glUseProgram(self.program_id)

    def clean_program(self):
        log.debug('cleaning up shader program')
        for shader_id in self.shader_ids:
            gl.glDetachShader(self.program_id, shader_id)
            gl.glDeleteShader(shader_id)
        gl.glUseProgram(0)
        gl.glDeleteProgram(self.program_id)