import os
from typing import Optional, Tuple


class Mesh:
    def __init__(
        self,
        file_name: Optional[str] = None,
        points: list[Tuple[int, float, float, float]] = [],
        faces: list[Tuple[int, int, int]] = [],
    ):
        self.file_name = file_name
        self.points = points
        self.faces = faces
        self.num_points: int = None

        if self.file_name is not None:
            self.load_data()

        self._get_num_of_points()

    def load_data(self):
        if not os.path.isfile(self.file_name):
            raise FileNotFoundError("File not found: {}".format(self.file_name))

        self._check_file_type()
        self._load()

    def write_data(self, file_name: str = None, prec: int = 4):
        if file_name is None:
            file_name = self.file_name

        self._write(file_name, prec)

    def _get_num_of_points(self):
        self.num_points = len(self.points)

    def _check_file_type(self):
        pass

    def _load(self):
        pass

    def _write(self, file_name: str, prec: int):
        pass
