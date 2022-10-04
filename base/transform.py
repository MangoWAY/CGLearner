import numpy as np
from scipy.spatial.transform import Rotation as R

class Transform:

    def __init__(self) -> None:
        self._eulerAngle = [0,0,0]
        self._pos = [0,0,0]
        self._scale = [1,1,1]

    @property
    def localPosition(self):
        return self._pos
        
    @localPosition.setter
    def localPosition(self, pos):
        self._pos = pos
    
    @property
    def localScale(self):
        return self._scale

    @localScale.setter
    def localScale(self, scale):
        self._scale = scale

    @property
    def localEulerAngle(self):
        return self._eulerAngle

    @localEulerAngle.setter
    def localEulerAngle(self,angle):
        # xyz
        self._eulerAngle = angle

    def localMatrix(self):
        mat = np.identity(4)
        for i in range(3):
            mat[i,i] = self._scale[i]
        rot = np.identity(4)
        rot[:3,:3] = R.from_euler("xyz", self._eulerAngle, degrees = True).as_matrix()
        mat = rot @ mat
        for i in range(3):
            mat[i,3] = self._pos[i]
        return mat

    def get_to_Local(self):
        mat = self.localMatrix()
        ori = np.identity(4)
        ori[:3,:3] = mat[:3,:3]
        ori = np.transpose(ori)
        pos = np.identity(4)
        pos[0:3,3] = -mat[0:3,3]
        return ori @ pos
        