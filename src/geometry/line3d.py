"""Immutable 3D line implementation for the HFC Geometry Kernel.

This module defines a lightweight, dependency-free representation of an
infinite line in 3D space. The line is stored by an origin point and a
normalized direction vector and supports point evaluation, projection,
measurement, geometric relations, and affine transformations.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .point3d import Point3D
from .precision_manager import PrecisionManager
from .transform3d import Transform3D
from .vector3d import Vector3D


@dataclass(frozen=True)
class Line3D:
    """Represent an immutable line in 3D space.

    The line is defined by an origin point and a direction vector that is
    automatically normalized during initialization. It supports point queries,
    projection, distance calculation, geometric relationships such as
    parallelism and perpendicularity, and affine transformations.
    """

    origin: Point3D
    direction: Vector3D

    def __post_init__(self) -> None:
        """Validate the line data and normalize the direction vector."""
        if not isinstance(self.origin, Point3D):
            raise TypeError("origin must be a Point3D")
        if not isinstance(self.direction, Vector3D):
            raise TypeError("direction must be a Vector3D")
        try:
            normalized_direction = self.direction.normalized()
        except ValueError as exc:
            raise ValueError("direction must not be a zero-length vector") from exc
        object.__setattr__(self, "direction", normalized_direction)

    @classmethod
    def from_points(cls, p1: Point3D, p2: Point3D) -> "Line3D":
        """Create a line passing through two points.

        Args:
            p1: The first point.
            p2: The second point.

        Returns:
            A line that passes through p1 and p2.

        Raises:
            TypeError: If either point is not a Point3D.
            ValueError: If the two points are identical.
        """
        if not isinstance(p1, Point3D):
            raise TypeError("p1 must be a Point3D")
        if not isinstance(p2, Point3D):
            raise TypeError("p2 must be a Point3D")
        if p1 == p2:
            raise ValueError("p1 and p2 must be distinct")
        direction = Vector3D(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
        return cls(p1, direction)

    @classmethod
    def from_point_direction(cls, origin: Point3D, direction: Vector3D) -> "Line3D":
        """Create a line from an origin point and a direction vector."""
        if not isinstance(origin, Point3D):
            raise TypeError("origin must be a Point3D")
        if not isinstance(direction, Vector3D):
            raise TypeError("direction must be a Vector3D")
        return cls(origin, direction)

    def point_at(self, t: float) -> Point3D:
        """Return the point at the given parametric coordinate along the line."""
        self._validate_scalar(t, "t")
        return Point3D(
            self.origin.x + float(t) * self.direction.x,
            self.origin.y + float(t) * self.direction.y,
            self.origin.z + float(t) * self.direction.z,
        )

    def contains(self, point: Point3D) -> bool:
        """Return True when the supplied point lies on the line."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")
        vector_to_point = Vector3D(point.x - self.origin.x, point.y - self.origin.y, point.z - self.origin.z)
        return vector_to_point.cross(self.direction) == Vector3D(0.0, 0.0, 0.0)

    def project_point(self, point: Point3D) -> Point3D:
        """Return the orthogonal projection of a point onto the line."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")
        vector_to_point = Vector3D(point.x - self.origin.x, point.y - self.origin.y, point.z - self.origin.z)
        t = vector_to_point.dot(self.direction)
        return self.point_at(t)

    def closest_point(self, point: Point3D) -> Point3D:
        """Return the closest point on the line to the supplied point."""
        return self.project_point(point)

    def distance_to_point(self, point: Point3D) -> float:
        """Return the Euclidean distance from the supplied point to the line."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")
        closest = self.closest_point(point)
        return closest.distance_to(point)

    def parallel_to(self, line: "Line3D") -> bool:
        """Return True when the supplied line is parallel to this line."""
        if not isinstance(line, Line3D):
            raise TypeError("line must be a Line3D")
        return self.direction.cross(line.direction) == Vector3D(0.0, 0.0, 0.0)

    def perpendicular_to(self, line: "Line3D") -> bool:
        """Return True when the supplied line is perpendicular to this line."""
        if not isinstance(line, Line3D):
            raise TypeError("line must be a Line3D")
        return self._precision_manager.compare_floats(self.direction.dot(line.direction), 0.0)

    def angle_to(self, line: "Line3D") -> float:
        """Return the angle between this line and another line in radians."""
        if not isinstance(line, Line3D):
            raise TypeError("line must be a Line3D")
        cosine = self.direction.dot(line.direction)
        cosine = max(-1.0, min(1.0, cosine))
        return math.acos(cosine)

    def reverse(self) -> "Line3D":
        """Return a line with the same geometry but opposite direction."""
        return Line3D(self.origin, Vector3D(-self.direction.x, -self.direction.y, -self.direction.z))

    def copy(self) -> "Line3D":
        """Return a copy of this line."""
        return Line3D(self.origin, self.direction)

    def transform(self, transform3d: Transform3D) -> "Line3D":
        """Return a transformed copy of this line."""
        if not isinstance(transform3d, Transform3D):
            raise TypeError("transform3d must be a Transform3D")
        return Line3D(
            transform3d.apply_to_point(self.origin),
            transform3d.apply_to_vector(self.direction),
        )

    @staticmethod
    def _validate_scalar(value: object, name: str) -> None:
        """Validate that a value is a real scalar."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a real number")

    _precision_manager = PrecisionManager()


__all__ = ["Line3D"]
