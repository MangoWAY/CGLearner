
class SubMesh:
    def __init__(self, indices) -> None:
        self.indices = indices

class Mesh:
    def __init__(self) -> None:
        self.vertices = []
        self.normals = []
        self.subMeshes = []
        self.uvs = []