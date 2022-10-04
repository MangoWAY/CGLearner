import glfw, logging, sys
from OpenGL import GL as gl
log = logging.getLogger(__name__)
class Window:

    class Config:
        def __init__(self,gl_version = (3,3), size = (500,400), title = "cglearn", bgcolor = (0,0.4,0)) -> None:
            self.gl_version = gl_version
            self.size = size
            self.title = title
            self.bgcolor = bgcolor
            
    def __init__(self,config: Config) -> None:
        self.native_window = None
        self.config = config
        self.init(config)

    def set_background(self,r,g,b):
        gl.glClearColor(r, g, b, 0)

    def init(self, config: Config):
        if not glfw.init():
            log.error('failed to initialize GLFW')
            sys.exit(1)
        log.debug('requiring modern OpenGL without any legacy features')
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, config.gl_version[0])
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, config.gl_version[1])
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        log.debug('opening window')
        self.native_window = glfw.create_window(config.size[0], config.size[1], config.title, None, None)
        if not self.native_window:
            log.error('failed to open GLFW window.')
            sys.exit(2)
        glfw.make_context_current(self.native_window)
        log.debug('set background to dark blue')
        gl.glClearColor(0, config.bgcolor[0], config.bgcolor[1],config.bgcolor[2])
    