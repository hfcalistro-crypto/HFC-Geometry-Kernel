"""Plane representation for the HFC Geometry Kernel.

This module defines an immutable 3D plane primitive with support for
construction from points, normalized coefficients, geometric queries,
transformations, and precision-aware comparisons.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Optional, Tuple

from .matrix4x4 import Matrix4x4
from .point3d import Point3D
from .precision_manager import PrecisionManager
from .transform3d import Transform3D
from .vector3d import Vector3D

PlaneIntersection = tuple[Point3D, Vector3D]


@dataclass(frozen=True)
class Plane3D:
    """Represent an immutable plane in 3D space.

    A plane is stored in normalized form such that its normal vector has unit
    length and the equation `ax + by + cz + d = 0` remains consistent.
    """

    normal: Vector3D
    point: Point3D
    d: float = field(init=False)

    _precision_manager: ClassVar[PrecisionManager] = PrecisionManager()

    def __post_init__(self) -> None:
        normalized = self._normalize_normal(self.normal)
        object.__setattr__(self, "normal", normalized)
        object.__setattr__(self, "point", self._validate_point(self.point))
        object.__setattr__(self, "d", self._compute_d(normalized, self.point))

    @classmethod
    def from_coefficients(
        cls,
        a: float,
        b: float,
        c: float,
        d: float,
    ) -> "Plane3D":
        """Create a plane from general coefficients.

        Args:
            a: Plane coefficient for x.
            b: Plane coefficient for y.
            c: Plane coefficient for z.
            d: Plane constant.

        Returns:
            A normalized Plane3D instance.
        """
        normal = Vector3D(a, b, c)
        if cls._precision_manager.compare_floats(normal.length(), 0.0):
            raise ValueError("Plane normal cannot be the zero vector")

        normalized = normal.normalized()
        magnitude = normal.length()
        normalized_d = float(d) / magnitude
        reference_point = Point3D(
            -normalized.x * normalized_d,
            -normalized.y * normalized_d,
            -normalized.z * normalized_d,
        )
        return cls(normalized, reference_point)

    @classmethod
    def from_points(
        cls,
        first: Point3D,
        second: Point3D,
        third: Point3D,
    ) -> "Plane3D":
        """Create a plane from three non-collinear points.

        Args:
            first: First point on the plane.
            second: Second point on the plane.
            third: Third point on the plane.

        Returns:
            A normalized Plane3D instance.
        """
        edge_one = Vector3D(
            second.x - first.x,
            second.y - first.y,
            second.z - first.z,
        )
        edge_two = Vector3D(
            third.x - first.x,
            third.y - first.y,
            third.z - first.z,
        )
        normal = edge_one.cross(edge_two)
        if cls._precision_manager.compare_floats(normal.length(), 0.0):
            raise ValueError("Points must not be collinear")
        return cls(normal, first)

    def normal_vector(self) -> Vector3D:
        """Return the unit normal vector of the plane."""
        return self.normal

    def point_on_plane(self) -> Point3D:
        """Return a point known to lie on the plane."""
        return self.point

    def distance_to_point(self, point: Point3D) -> float:
        """Return the absolute distance from a point to the plane."""
        return abs(self.signed_distance_to_point(point))

    def signed_distance_to_point(self, point: Point3D) -> float:
        """Return the signed distance from a point to the plane."""
        return (
            self.normal.x * point.x
            + self.normal.y * point.y
            + self.normal.z * point.z
            + self.d
        )

    def project_point(self, point: Point3D) -> Point3D:
        """Return the orthogonal projection of a point onto the plane."""
        signed_distance = self.signed_distance_to_point(point)
        return Point3D(
            point.x - signed_distance * self.normal.x,
            point.y - signed_distance * self.normal.y,
            point.z - signed_distance * self.normal.z,
        )

    def is_point_on_plane(
        self,
        point: Point3D,
        tolerance: float | None = None,
    ) -> bool:
        """Return whether a point lies on the plane within tolerance."""
        tolerance = self._precision_manager.get_linear_tolerance() if tolerance is None else tolerance
        return self._precision_manager.compare_floats(
            self.signed_distance_to_point(point),
            0.0,
            tolerance=tolerance,
        )

    def is_parallel_to(self, other: "Plane3D") -> bool:
        """Return whether this plane is parallel to another plane."""
        if not isinstance(other, Plane3D):
            raise TypeError("Comparison requires a Plane3D instance")
        return self._precision_manager.compare_floats(
            abs(self.normal.dot(other.normal)),
            1.0,
        )

    def is_orthogonal_to(self, other: "Plane3D") -> bool:
        """Return whether this plane is orthogonal to another plane."""
        if not isinstance(other, Plane3D):
            raise TypeError("Comparison requires a Plane3D instance")
        return self._precision_manager.compare_floats(
            self.normal.dot(other.normal),
            0.0,
        )

    def intersect_with_plane(
        self,
        other: "Plane3D",
    ) -> Optional[PlaneIntersection]:
        """Return a point and direction for the intersection line with another plane.

        Returns None when the planes are parallel or coincident.
        """
        if not isinstance(other, Plane3D):
            raise TypeError("Intersection requires a Plane3D instance")

        if self.is_parallel_to(other):
            return None

        direction = self.normal.cross(other.normal)
        denominator = direction.length() ** 2
        if self._precision_manager.compare_floats(denominator, 0.0):
            return None

        numerator = (
            other.normal.cross(direction) * (-self.d)
            + direction.cross(self.normal) * (-other.d)
        )
        intersection_point = Point3D(
            numerator.x / denominator,
            numerator.y / denominator,
            numerator.z / denominator,
        )
        return intersection_point, direction

    def apply_transform(self, transform: Transform3D) -> "Plane3D":
        """Return a new plane transformed by the given Transform3D."""
        return self.apply_matrix(transform.to_matrix())

    def apply_matrix(self, matrix: Matrix4x4) -> "Plane3D":
        """Return a new plane transformed by the given Matrix4x4."""
        transformed_point = matrix * self.point
        transformed_normal = self._transform_normal(self.normal, matrix)
        return Plane3D(transformed_normal, transformed_point)

    def to_coefficients(self) -> tuple[float, float, float, float]:
        """Return the plane coefficients (a, b, c, d)."""
        return (self.normal.x, self.normal.y, self.normal.z, self.d)

    def to_string(self) -> str:
        """Return a human-readable string representation of the plane."""
        a, b, c, d = self.to_coefficients()
        return f"Plane3D({a:.6f}x + {b:.6f}y + {c:.6f}z + {d:.6f} = 0)"

    def __eq__(self, other: object) -> bool:
        """Compare two planes using the HGK precision policy."""
        if not isinstance(other, Plane3D):
            return NotImplemented

        same_orientation = self._precision_manager.compare_vectors(
            self.normal.to_tuple(),
            other.normal.to_tuple(),
        ) and self._precision_manager.compare_floats(self.d, other.d)

        opposite_orientation = self._precision_manager.compare_vectors(
            self.normal.to_tuple(),
            (other.normal * -1.0).to_tuple(),
        ) and self._precision_manager.compare_floats(self.d, -other.d)

        return same_orientation or opposite_orientation

    def normalize(self) -> "Plane3D":
        """Return a normalized plane. The current plane is already normalized."""
        return self

    def flip(self) -> "Plane3D":
        """Return a new plane with inverted orientation."""
        return Plane3D(self.normal * -1.0, self.point)

    def _normalize_normal(self, normal: Vector3D) -> Vector3D:
        if not isinstance(normal, Vector3D):
            raise TypeError("Plane normal must be a Vector3D")
        if self._precision_manager.compare_floats(normal.length(), 0.0):
            raise ValueError("Plane normal cannot be the zero vector")

        normalized = normal.normalized()
        if self._should_flip_orientation(normalized):
            normalized = normalized * -1.0
        return normalized

    def _compute_d(self, normal: Vector3D, point: Point3D) -> float:
        return -(
            normal.x * point.x
            + normal.y * point.y
            + normal.z * point.z
        )

    def _validate_point(self, point: Point3D) -> Point3D:
        if not isinstance(point, Point3D):
            raise TypeError("Plane point must be a Point3D")
        return point

    def _should_flip_orientation(self, normal: Vector3D) -> bool:
        if normal.x < 0.0:
            return True
        if self._precision_manager.compare_floats(normal.x, 0.0):
            if normal.y < 0.0:
                return True
            if self._precision_manager.compare_floats(normal.y, 0.0) and normal.z < 0.0:
                return True
        return False

    def _transform_normal(self, normal: Vector3D, matrix: Matrix4x4) -> Vector3D:
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


__all__ = ["Plane3D"]
