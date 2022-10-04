# pyassimp 4.1.4 has some problem will lead to randomly crash, use 4.1.3 to fix
# should set link path to find the dylib

import pyassimp
import numpy as np
from .mesh import Mesh, SubMesh

class ModelImporter:
    def __init__(self) -> None:
        pass

    def load_mesh(self, path: str):
        scene = pyassimp.load(path)
        mmeshes = []
        for mesh in scene.meshes:
            mmesh = Mesh()
            mmesh.vertices = np.reshape(np.copy(mesh.vertices), (1,-1)).squeeze(0) /200
            mmesh.normals = np.reshape(np.copy(mesh.normals),(1,-1)).squeeze(0)
            mmesh.subMeshes = []
            mmesh.subMeshes.append(SubMesh(np.reshape(np.copy(mesh.faces), (1,-1)).squeeze(0)))
            mmeshes.append(mmesh)
        return mmeshes