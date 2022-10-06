

from OpenGL import GL as gl
from PIL import Image
import numpy as np
class Texture:
    COUNT = 0
    def __init__(self) -> None:
        self.texid = -1
        self.count = -1

    def create(self):
        self.texid = gl.glGenTextures(1)
        
    def load_from_path(self, path: str):
        gl.glActiveTexture(gl.GL_TEXTURE0 + Texture.COUNT)
        self.count = Texture.COUNT
        Texture.COUNT +=1
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texid)
        # Set the texture wrapping parameters
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        # Set texture filtering parameters
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        # load image
        image = Image.open(path)
        img_data = np.array(list(image.getdata()), np.uint8)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 
                        0, 
                        gl.GL_RGB, 
                        image.width, 
                        image.height, 
                        0, 
                        gl.GL_RGB, 
                        gl.GL_UNSIGNED_BYTE, 
                        img_data)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    def bind(self):
        gl.glActiveTexture(gl.GL_TEXTURE0 + self.count)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texid)

