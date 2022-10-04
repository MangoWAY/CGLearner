from math import cos, sin
import math
import numpy as np

class Camera:
    def __init__(self) -> None:
        self._fov = 60
        self._near = 0.3
        self._far = 1000
        self._aspect = 5 / 4

    @property
    def fov(self):
        return self._fov
    
    @fov.setter
    def fov(self, fov):
        self._fov = fov

    @property
    def near(self):
        return self._near

    @near.setter
    def near(self, near):
        self._near = near
    
    def getProjectionMatrix(self):
        r = math.radians(self._fov / 2)
        cotangent = cos(r) / sin(r)
        deltaZ = self._near - self._far
        projection = np.zeros((4,4))
        projection[0,0] = cotangent / self._aspect
        projection[1,1] = cotangent
        projection[2,2] = (self._near + self._far) / deltaZ
        projection[2,3] = 2 * self._near * self._far / deltaZ
        projection[3,2] = -1
        return projection
