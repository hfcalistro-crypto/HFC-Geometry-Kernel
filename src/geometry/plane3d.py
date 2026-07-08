"""Immutable 3D plane implementation for the HFC Geometry Kernel.

The plane is represented by a reference point and a normalized normal vector.
It supports construction from a point and normal, three points, or a plane
equation, along with distance queries, projection, intersections, and affine
transformations using HGK precision rules.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import ClassVar

from .line3d import Line3D
from .matrix4x4 import Matrix4x4
from .point3d import Point3D
from .precision_manager import PrecisionManager
from .transform3d import Transform3D
from .vector3d import Vector3D


@dataclass(frozen=True)
class Plane3D:
    """Represent an immutable plane in 3D space.

    The plane is defined by a point that lies on the plane and a normal vector.
    The normal is normalized on initialization so the plane always uses a unit
    normal vector internally.
    """

    point: Point3D
    normal: Vector3D

    d: float = field(init=False, repr=False)

    _precision_manager: ClassVar[PrecisionManager] = PrecisionManager()

    def __post_init__(self) -> None:
        """Validate the plane inputs and normalize the stored normal."""
        if not isinstance(self.point, Point3D):
            raise TypeError("point must be a Point3D")
        if not isinstance(self.normal, Vector3D):
            raise TypeError("normal must be a Vector3D")

        try:
            normalized_normal = self.normal.normalized()
        except ValueError as exc:
            raise ValueError("normal must not be a zero-length vector") from exc

        object.__setattr__(self, "normal", normalized_normal)
        object.__setattr__(self, "d", self._compute_d(normalized_normal, self.point))

    @classmethod
    def from_point_normal(cls, point: Point3D, normal: Vector3D) -> "Plane3D":
        """Create a plane from a point belonging to it and a normal vector."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")
        if not isinstance(normal, Vector3D):
            raise TypeError("normal must be a Vector3D")
        return cls(point, normal)

    @classmethod
    def from_points(cls, p1: Point3D, p2: Point3D, p3: Point3D) -> "Plane3D":
        """Create a plane from three non-collinear points."""
        if not isinstance(p1, Point3D):
            raise TypeError("p1 must be a Point3D")
        if not isinstance(p2, Point3D):
            raise TypeError("p2 must be a Point3D")
        if not isinstance(p3, Point3D):
            raise TypeError("p3 must be a Point3D")

        edge_one = Vector3D(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
        edge_two = Vector3D(p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
        normal = edge_one.cross(edge_two)
        if cls._precision_manager.compare_floats(normal.length(), 0.0):
            raise ValueError("p1, p2, and p3 must not be collinear")
        return cls(p1, normal)

    @classmethod
    def from_equation(cls, a: float, b: float, c: float, d: float) -> "Plane3D":
        """Create a plane from the general equation $ax + by + cz + d = 0$."""
        cls._validate_scalar(a, "a")
        cls._validate_scalar(b, "b")
        cls._validate_scalar(c, "c")
        cls._validate_scalar(d, "d")

        normal = Vector3D(float(a), float(b), float(c))
        if cls._precision_manager.compare_floats(normal.length(), 0.0):
            raise ValueError("Plane normal cannot be the zero vector")

        normalized_normal = normal.normalized()
        magnitude = normal.length()
        normalized_d = float(d) / magnitude
        point = Point3D(
            -normalized_normal.x * normalized_d,
            -normalized_normal.y * normalized_d,
            -normalized_normal.z * normalized_d,
        )
        return cls(point, normalized_normal)

    @classmethod
    def from_coefficients(cls, a: float, b: float, c: float, d: float) -> "Plane3D":
        """Backward-compatible alias for from_equation."""
        return cls.from_equation(a, b, c, d)

    def signed_distance(self, point: Point3D) -> float:
        """Return the signed distance from a point to the plane."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")
        return (
            self.normal.x * point.x
            + self.normal.y * point.y
            + self.normal.z * point.z
            + self.d
        )

    def distance_to_point(self, point: Point3D) -> float:
        """Return the absolute distance from a point to the plane."""
        return abs(self.signed_distance(point))

    def contains(self, point: Point3D) -> bool:
        """Return True when the supplied point lies on the plane."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")
        return self._precision_manager.compare_floats(self.signed_distance(point), 0.0)

    def project_point(self, point: Point3D) -> Point3D:
        """Return the orthogonal projection of a point onto the plane."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")
        signed_distance = self.signed_distance(point)
        return Point3D(
            point.x - signed_distance * self.normal.x,
            point.y - signed_distance * self.normal.y,
            point.z - signed_distance * self.normal.z,
        )

    def closest_point(self, point: Point3D) -> Point3D:
        """Return the closest point on the plane to the supplied point."""
        return self.project_point(point)

    def intersect_line(self, line: Line3D) -> Point3D | None:
        """Return the intersection point between the plane and a line, if any."""
        if not isinstance(line, Line3D):
            raise TypeError("line must be a Line3D")

        origin_distance = self.signed_distance(line.origin)
        denominator = self.normal.dot(line.direction)
        if self._precision_manager.compare_floats(denominator, 0.0):
            if self._precision_manager.compare_floats(origin_distance, 0.0):
                return line.origin
            return None

        parameter = -origin_distance / denominator
        return line.point_at(parameter)

    def angle_to_line(self, line: Line3D) -> float:
        """Return the angle between the plane and a line in radians."""
        if not isinstance(line, Line3D):
            raise TypeError("line must be a Line3D")

        cosine = abs(self.normal.dot(line.direction))
        cosine = max(0.0, min(1.0, cosine))
        return math.asin(cosine)

    def angle_to_plane(self, plane: "Plane3D") -> float:
        """Return the acute angle between this plane and another plane in radians."""
        if not isinstance(plane, Plane3D):
            raise TypeError("plane must be a Plane3D")

        cosine = abs(self.normal.dot(plane.normal))
        cosine = max(0.0, min(1.0, cosine))
        return math.acos(cosine)

    def flip(self) -> "Plane3D":
        """Return a plane with the opposite orientation."""
        return Plane3D(self.point, self.normal.scaled(-1.0))

    def transform(self, transform3d: Transform3D) -> "Plane3D":
        """Return a transformed copy of the plane."""
        if not isinstance(transform3d, Transform3D):
            raise TypeError("transform3d must be a Transform3D")

        transformed_point = transform3d.apply_to_point(self.point)
        transformed_normal = self._transform_normal(self.normal, transform3d.to_matrix())
        return Plane3D(transformed_point, transformed_normal)

    def normalize(self) -> "Plane3D":
        """Return this plane unchanged because it is already normalized."""
        return self

    def copy(self) -> "Plane3D":
        """Return a copy of the plane."""
        return Plane3D(self.point, self.normal)

    def signed_distance_to_point(self, point: Point3D) -> float:
        """Backward-compatible wrapper for signed_distance."""
        return self.signed_distance(point)

    def is_point_on_plane(self, point: Point3D) -> bool:
        """Backward-compatible wrapper for contains."""
        return self.contains(point)

    def is_parallel_to(self, other: "Plane3D") -> bool:
        """Return True when two planes are parallel."""
        if not isinstance(other, Plane3D):
            raise TypeError("other must be a Plane3D")
        return self._precision_manager.compare_floats(abs(self.normal.dot(other.normal)), 1.0)

    def is_orthogonal_to(self, other: "Plane3D") -> bool:
        """Return True when two planes are orthogonal."""
        if not isinstance(other, Plane3D):
            raise TypeError("other must be a Plane3D")
        return self._precision_manager.compare_floats(self.normal.dot(other.normal), 0.0)

    def intersect_with_plane(self, other: "Plane3D") -> tuple[Point3D, Vector3D] | None:
        """Return the line of intersection between two planes, if one exists."""
        if not isinstance(other, Plane3D):
            raise TypeError("other must be a Plane3D")

        direction = self.normal.cross(other.normal)
        if self._precision_manager.compare_floats(direction.length(), 0.0):
            return None

        point = self._intersection_point(other, direction)
        return point, direction

    def apply_transform(self, transform3d: Transform3D) -> "Plane3D":
        """Backward-compatible wrapper for transform."""
        return self.transform(transform3d)

    def apply_matrix(self, matrix: Matrix4x4) -> "Plane3D":
        """Apply a 4x4 affine matrix to the plane."""
        if not isinstance(matrix, Matrix4x4):
            raise TypeError("matrix must be a Matrix4x4")
        return Plane3D(
            matrix * self.point,
            self._transform_normal(self.normal, matrix),
        )

    def to_coefficients(self) -> tuple[float, float, float, float]:
        """Return the plane coefficients as $(a, b, c, d)$."""
        return (self.normal.x, self.normal.y, self.normal.z, self.d)

    def to_string(self) -> str:
        """Return a human-readable string representation of the plane."""
        a, b, c, d = self.to_coefficients()
        return f"Plane3D({a:.6f}x + {b:.6f}y + {c:.6f}z + {d:.6f} = 0)"

    def __eq__(self, other: object) -> bool:
        """Compare two planes using HGK precision rules."""
        if not isinstance(other, Plane3D):
            return NotImplemented

        return (
            self._precision_manager.compare_points(self.point.to_tuple(), other.point.to_tuple())
            and self._precision_manager.compare_vectors(self.normal.to_tuple(), other.normal.to_tuple())
        )

    @staticmethod
    def _validate_scalar(value: object, name: str) -> None:
        """Validate that the supplied value is a real scalar."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a real number")

    @staticmethod
    def _compute_d(normal: Vector3D, point: Point3D) -> float:
        """Compute the constant term in the plane equation."""
        return -(normal.x * point.x + normal.y * point.y + normal.z * point.z)

    def _transform_normal(self, normal: Vector3D, matrix: Matrix4x4) -> Vector3D:
        """Transform a plane normal with the inverse-transpose of the linear part."""
        linear_part = [
            [matrix.rows[row][col] for col in range(3)]
            for row in range(3)
        ]
        inverse_linear = self._invert_3x3(linear_part)
        transpose_inverse = [
            [inverse_linear[col][row] for col in range(3)]
            for row in range(3)
        ]

        transformed_x = (
            transpose_inverse[0][0] * normal.x
            + transpose_inverse[0][1] * normal.y
            + transpose_inverse[0][2] * normal.z
        )
        transformed_y = (
            transpose_inverse[1][0] * normal.x
            + transpose_inverse[1][1] * normal.y
            + transpose_inverse[1][2] * normal.z
        )
        transformed_z = (
            transpose_inverse[2][0] * normal.x
            + transpose_inverse[2][1] * normal.y
            + transpose_inverse[2][2] * normal.z
        )
        transformed_normal = Vector3D(transformed_x, transformed_y, transformed_z)
        if self._precision_manager.compare_floats(transformed_normal.length(), 0.0):
            raise ValueError("Transformed normal is degenerate")
        return transformed_normal.normalized()

    def _invert_3x3(self, matrix: list[list[float]]) -> list[list[float]]:
        """Return the inverse of a 3x3 matrix."""
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        determinant = (
            a * (e * i - f * h)
            - b * (d * i - f * g)
            + c * (d * h - e * g)
        )
        if self._precision_manager.compare_floats(determinant, 0.0):
            raise ValueError("Matrix is not invertible")

        inverse_factor = 1.0 / determinant
        return [
            [
                (e * i - f * h) * inverse_factor,
                (c * h - b * i) * inverse_factor,
                (b * f - c * e) * inverse_factor,
            ],
            [
                (f * g - d * i) * inverse_factor,
                (a * i - c * g) * inverse_factor,
                (c * d - a * f) * inverse_factor,
            ],
            [
                (d * h - e * g) * inverse_factor,
                (b * g - a * h) * inverse_factor,
                (a * e - b * d) * inverse_factor,
            ],
        ]

    def _intersection_point(self, other: "Plane3D", direction: Vector3D) -> Point3D:
        """Compute a point on the line that results from intersecting two planes."""
        denominator = direction.length() * direction.length()
        cross = self.normal.cross(other.normal)
        point = Point3D(
            (cross.x * (self.d - other.d)) / denominator,
            (cross.y * (self.d - other.d)) / denominator,
            (cross.z * (self.d - other.d)) / denominator,
        )
        return point


__all__ = ["Plane3D"]
