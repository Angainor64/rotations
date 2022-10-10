from typing import List, Tuple, Dict
from math import sqrt, sin, cos
from turtle import Turtle
import turtle as t
import numpy as np


EPS = 1e-6


class PointND:
    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        raise AttributeError(
            "'dimensions' attribute of 'PointND' object is non-mutable"
        )

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: Tuple[int | float, ...]):
        if len(value) != self.dimensions:
            raise TypeError(
                f"new value for 'pos' must have dimension {self.dimensions}"
            )
        self._pos = value

    def __init__(self, dimensions: int, pos: Tuple[float | int, ...]):
        self._dimensions = dimensions
        self._pos = pos

    def __sub__(self, other) -> "PointND":
        if not isinstance(other, PointND):
            raise TypeError(
                f"unsupported operand type(s) for -: '{self.__class__}' and '{other.__class__}'"
            )
        if self.dimensions != other.dimensions:
            raise TypeError(
                f"operations between two 'PointND' objects of different dimensions not supported"
            )
        return PointND(
            self.dimensions,
            tuple([self.pos[i] - other.pos[i] for i in range(self.dimensions)]),
        )

    def __add__(self, other) -> "PointND":
        if not isinstance(other, PointND):
            raise TypeError(
                f"unsupported operand type(s) for +: '{self.__class__}' and '{other.__class__}'"
            )
        if self.dimensions != other.dimensions:
            raise TypeError(
                f"operations between two 'PointND' objects of different dimensions not supported"
            )
        return PointND(
            self.dimensions,
            tuple([self.pos[i] + other.pos[i] for i in range(self.dimensions)]),
        )

    def rotate(self, rot_matrix: Tuple[Tuple[int | float, ...], ...]) -> None:
        self.pos = tuple(np.cross(rot_matrix, np.asarray(self.pos)))


class VectorND(PointND):
    def __abs__(self):
        return sqrt(sum(map(lambda a: a**2, self.pos)))

    def __truediv__(self, other) -> "VectorND":
        if not (isinstance(other, float) or isinstance(other, int)):
            raise TypeError(
                f"unsupported operand type(s) for /: '{self.__class__}' and '{other.__class__}'"
            )
        return VectorND(self.dimensions, tuple(map(lambda a: a / other, self.pos)))

    def __mul__(self, other) -> "VectorND":
        if isinstance(other, float) or isinstance(other, int):
            return VectorND(self.dimensions, tuple(map(lambda a: a * other, self.pos)))
        raise TypeError(
            f"unsupported operand type(s) for *: '{self.__class__}' and '{other.__class__}'"
        )

    def __neg__(self) -> "VectorND":
        return VectorND(self.dimensions, tuple(map(lambda a: -a, self.pos)))

    @classmethod
    def cross(cls, vector_a: "VectorND", vector_b: "VectorND") -> "VectorND":
        if vector_a.dimensions != vector_b.dimensions:
            raise TypeError(
                f"operations between two 'VectorND' objects of different dimensions not supported"
            )
        return VectorND(
            vector_a.dimensions, tuple(np.cross(vector_a.pos, vector_b.pos))
        )

    @classmethod
    def dot(cls, vector_a: "VectorND", vector_b: "VectorND") -> float:
        if vector_a.dimensions != vector_b.dimensions:
            raise TypeError(
                f"operations between two 'VectorND' objects of different dimensions not supported"
            )
        return float(np.dot(vector_a.pos, vector_b.pos))


class LineND:
    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        raise AttributeError("'dimensions' attribute of 'LineND' object is non-mutable")

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, value):
        raise AttributeError("'vector' attribute of 'LineND' object is non-mutable")

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, value):
        raise AttributeError("'point' attribute of 'LineND' object is non-mutable")

    def __init__(self, dimensions: int, point_0: PointND, point_1: PointND):
        if point_0.dimensions != dimensions:
            raise TypeError("'point_0' must have same number of dimensions as line")
        if point_1.dimensions != dimensions:
            raise TypeError("'point_1' must have same number of dimensions as line")
        self._dimensions = dimensions
        self._point = point_0
        vector = VectorND(dimensions, (point_1 - point_0).pos)
        self._vector = vector / abs(vector)
        assert abs(self.vector) - 1 < EPS

    def get_point(self, t: float | int) -> PointND:
        return self.point + self.vector * t


class PlaneND:
    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        raise AttributeError(
            "'dimensions' attribute of 'PlaneND' object is non-mutable"
        )

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, value):
        raise AttributeError(
            "'dimensions' attribute of 'PlaneND' object is non-mutable"
        )

    @property
    def vector_0(self):
        return self._vector_0

    @vector_0.setter
    def vector_0(self, value):
        raise AttributeError("'vector_0' attribute of 'PlaneND' object is non-mutable")

    @property
    def vector_1(self):
        return self._vector_1

    @vector_1.setter
    def vector_1(self, value):
        raise AttributeError("'vector_1' attribute of 'PlaneND' object is non-mutable")

    def __init__(
        self, dimensions: int, point_0: PointND, point_1: PointND, point_2: PointND
    ):
        if point_0.dimensions != dimensions:
            raise TypeError("'point_0' must have same number of dimensions as line")
        if point_1.dimensions != dimensions:
            raise TypeError("'point_1' must have same number of dimensions as line")
        if point_2.dimensions != dimensions:
            raise TypeError("'point_2' must have same number of dimensions as line")
        self._dimensions = dimensions
        self._point = point_0
        vector = VectorND(dimensions, (point_1 - point_0).pos)
        self._vector_0 = vector / abs(vector)
        assert abs(self.vector_0) - 1 < EPS
        vector = VectorND(dimensions, (point_2 - point_0).pos)
        self._vector_1 = vector / abs(vector)
        assert abs(self.vector_1) - 1 < EPS

    def get_point(self, t: float | int, u: float | int) -> PointND:
        return self.point + self.vector_0 * t + self.vector_1 * u

    def get_intersection(self, line: LineND) -> PointND:
        if self.dimensions != line.dimensions:
            raise TypeError("'line' must have same number of dimensions as plane")
        t = VectorND.dot(
            VectorND.cross(self.vector_0, self.vector_1), line.point - self.point
        ) / VectorND.dot(-line.vector, VectorND.cross(self.vector_0, self.vector_1))
        return line.get_point(t)


class ShapeND:
    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        raise AttributeError(
            "'dimensions' attribute of 'ShapeND' object is non-mutable"
        )

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        raise TypeError(
            f"type '{self.__class__}' does not support assignment to attribute 'points'"
        )

    def __init__(self, dimensions: int, points: List[PointND] | Tuple[PointND]):
        self._points: Tuple[PointND] = tuple(points)
        self._dimensions = dimensions

    def rotate(self, rot_matrix: Tuple[Tuple[int | float, ...], ...]) -> None:
        for point in self.points:
            point.rotate(rot_matrix)


class DisplayShapeND(ShapeND):
    @property
    def displayed_points(self):
        return self._displayed_points

    @displayed_points.setter
    def displayed_points(self, value):
        raise TypeError(
            f"type '{self.__class__}' does not support assignment to attribute 'displayed_points'"
        )

    def __init__(
        self,
        dimensions: int,
        points: Dict[str, PointND],
        connections: Dict[str, List[str]],
    ):
        super(DisplayShapeND, self).__init__(dimensions, tuple(points.values()))
        self._displayed_points: Dict[str, Turtle] = {}
        for point in points:
            temp = Turtle(shape="circle")
            temp.pu()
            self.displayed_points[point] = temp

    def display(
        self, camera: PointND, viewing_plane: PlaneND, draw_lines: bool = True
    ) -> None:
        ...


def make_3d_rot_matrix(
    a: float, b: float, y: float
) -> Tuple[
    Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]
]:
    return (
        (
            cos(b) * cos(y),
            sin(a) * sin(b) * cos(y) - cos(a) * sin(y),
            cos(a) * sin(b) * cos(y) + sin(a) * sin(y),
        ),
        (
            cos(b) * cos(y),
            sin(a) * sin(b) * cos(y) + cos(a) * sin(y),
            cos(a) * sin(b) * cos(y) - sin(a) * sin(y),
        ),
        (
            -sin(b),
            sin(a) * cos(b),
            cos(a) * cos(b),
        ),
    )


if __name__ == "__main__":
    camera = PointND(3, (0, 0, -400))
    viewing_plane = PlaneND(
        3, PointND(3, (0, 0, -200)), PointND(3, (0, 1, -200)), PointND(3, (1, 0, -200))
    )
    cube = []
    vals = (-100, 100)
    for x in vals:
        for y in vals:
            for z in vals:
                cube.append(PointND(3, (x, y, z)))
    cube_display = ""
