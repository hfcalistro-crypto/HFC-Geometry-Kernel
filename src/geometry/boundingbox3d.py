"""Immutable axis-aligned 3D bounding box implementation for the HFC Geometry Kernel.

The bounding box is represented as a pair of minimum and maximum corner
points. It is immutable, dependency-free, and uses Point3D for all geometric
operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .point3d import Point3D


@dataclass(frozen=True)
class BoundingBox3D:
    """Represent an immutable axis-aligned bounding box in 3D space.

    The box stores its minimum and maximum corners as Point3D values. The
    implementation supports creation from a set of points, expansion with an
    additional point, containment queries, center and size computation, volume
    calculation, union/intersection operations, and copying.
    """

    min_point: Point3D
    max_point: Point3D

    def __post_init__(self) -> None:
        """Validate the bounding box corners and normalize them."""
        if not isinstance(self.min_point, Point3D):
            raise TypeError("min_point must be a Point3D")
        if not isinstance(self.max_point, Point3D):
            raise TypeError("max_point must be a Point3D")
        if self.min_point.x > self.max_point.x or self.min_point.y > self.max_point.y or self.min_point.z > self.max_point.z:
            raise ValueError("min_point must be less than or equal to max_point")

    @classmethod
    def empty(cls) -> "BoundingBox3D":
        """Return an empty bounding box instance."""
        return cls(Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0))

    @classmethod
    def from_points(cls, points: Sequence[Point3D]) -> "BoundingBox3D":
        """Create a bounding box that contains the provided points.

        Args:
            points: A sequence of Point3D instances.

        Raises:
            TypeError: If any item is not a Point3D.
            ValueError: If the sequence is empty.
        """
        if not isinstance(points, (list, tuple)):
            raise TypeError("points must be a sequence of Point3D")
        if len(points) == 0:
            raise ValueError("points must not be empty")

        normalized_points: list[Point3D] = []
        for point in points:
            if not isinstance(point, Point3D):
                raise TypeError("points must contain only Point3D instances")
            normalized_points.append(point)

        min_x = min(point.x for point in normalized_points)
        min_y = min(point.y for point in normalized_points)
        min_z = min(point.z for point in normalized_points)
        max_x = max(point.x for point in normalized_points)
        max_y = max(point.y for point in normalized_points)
        max_z = max(point.z for point in normalized_points)

        return cls(Point3D(min_x, min_y, min_z), Point3D(max_x, max_y, max_z))

    def expand(self, point: Point3D) -> "BoundingBox3D":
        """Return a new box expanded to include the provided point."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")

        if self.is_empty():
            return BoundingBox3D(point, point)

        return BoundingBox3D(
            Point3D(min(self.min_point.x, point.x), min(self.min_point.y, point.y), min(self.min_point.z, point.z)),
            Point3D(max(self.max_point.x, point.x), max(self.max_point.y, point.y), max(self.max_point.z, point.z)),
        )

    def contains(self, point: Point3D) -> bool:
        """Return True when the supplied point is inside the box."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")
        if self.is_empty():
            return False
        return (
            self.min_point.x <= point.x <= self.max_point.x
            and self.min_point.y <= point.y <= self.max_point.y
            and self.min_point.z <= point.z <= self.max_point.z
        )

    def center(self) -> Point3D:
        """Return the center point of the bounding box."""
        if self.is_empty():
            raise ValueError("Cannot compute center of an empty bounding box")
        return Point3D(
            (self.min_point.x + self.max_point.x) / 2.0,
            (self.min_point.y + self.max_point.y) / 2.0,
            (self.min_point.z + self.max_point.z) / 2.0,
        )

    def size(self) -> tuple[float, float, float]:
        """Return the dimensions of the box as a tuple of $(width, height, depth)$."""
        if self.is_empty():
            return (0.0, 0.0, 0.0)
        return (self.width(), self.height(), self.depth())

    def width(self) -> float:
        """Return the width of the box along the x axis."""
        return self.max_point.x - self.min_point.x

    def height(self) -> float:
        """Return the height of the box along the y axis."""
        return self.max_point.y - self.min_point.y

    def depth(self) -> float:
        """Return the depth of the box along the z axis."""
        return self.max_point.z - self.min_point.z

    def volume(self) -> float:
        """Return the volume of the box."""
        if self.is_empty():
            return 0.0
        return self.width() * self.height() * self.depth()

    def is_empty(self) -> bool:
        """Return True when the box has zero extent."""
        return self.min_point == self.max_point

    def union(self, other: "BoundingBox3D") -> "BoundingBox3D":
        """Return the union of this box and another box."""
        if not isinstance(other, BoundingBox3D):
            raise TypeError("other must be a BoundingBox3D")
        if self.is_empty():
            return other.copy()
        if other.is_empty():
            return self.copy()
        return BoundingBox3D(
            Point3D(min(self.min_point.x, other.min_point.x), min(self.min_point.y, other.min_point.y), min(self.min_point.z, other.min_point.z)),
            Point3D(max(self.max_point.x, other.max_point.x), max(self.max_point.y, other.max_point.y), max(self.max_point.z, other.max_point.z)),
        )

    def intersects(self, other: "BoundingBox3D") -> bool:
        """Return True when this box overlaps the other box."""
        if not isinstance(other, BoundingBox3D):
            raise TypeError("other must be a BoundingBox3D")
        if self.is_empty() or other.is_empty():
            return False
        return (
            self.min_point.x <= other.max_point.x
            and self.max_point.x >= other.min_point.x
            and self.min_point.y <= other.max_point.y
            and self.max_point.y >= other.min_point.y
            and self.min_point.z <= other.max_point.z
            and self.max_point.z >= other.min_point.z
        )

    def copy(self) -> "BoundingBox3D":
        """Return a copy of this bounding box."""
        return BoundingBox3D(self.min_point, self.max_point)


__all__ = ["BoundingBox3D"]
