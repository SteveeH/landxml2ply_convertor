import numpy as np
import open3d as o3d
from mesh import Mesh
from typing import Tuple, Optional


class Ply(Mesh):
    def __init__(
        self,
        file_name: Optional[str] = None,
        points: list[Tuple[int, float, float, float]] = [],
        faces: list[Tuple[int, int, int]] = [],
    ):
        super().__init__(file_name, points, faces)

    def _check_file_type(self):
        if not self.file_name.endswith(".ply"):
            raise TypeError("File is not a .ply file: {}".format(self.file_name))

    def _load(self):
        """
        Loads mesh data from a .ply file
        """

        mesh = o3d.io.read_triangle_mesh(self.file_name)
        mesh_points = np.asarray(mesh.vertices)
        indices = np.arange(0, len(mesh_points)).reshape(len(mesh_points), 1)

        self.points = np.hstack((indices, mesh.vertices)).tolist()
        self.faces = np.asarray(mesh.triangles).tolist()

    def _write(self, file_name: str, *args, **kwargs):
        """
        Writes mesh data to a .ply file
        """

        print(f"Writing data to PLY - {file_name}")
        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(np.asarray(self.points)[:, 1:])
        mesh.triangles = o3d.utility.Vector3iVector(np.asanyarray(self.faces))
        o3d.io.write_triangle_mesh(file_name, mesh)
