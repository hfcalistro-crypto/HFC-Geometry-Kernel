"""Immutable 3D point implementation for the HFC Geometry Kernel.

This module defines a small, dependency-free representation of a
3D point that can be used by higher-level geometric components.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .precision_manager import PrecisionManager


@dataclass(frozen=True)
class Point3D:
    """Represent an immutable 3D point in double precision.

    The class stores spatial coordinates in a compact, immutable form and
    provides basic geometric operations such as distance calculation,
    tuple conversion, translation, and equality based on the HGK precision
    policy.
    """

    x: float
    y: float
    z: float

    _precision_manager: Final[PrecisionManager] = PrecisionManager()

    def __post_init__(self) -> None:
        """Normalize the stored coordinates to double precision values."""
        object.__setattr__(self, "x", float(self.x))
        object.__setattr__(self, "y", float(self.y))
        object.__setattr__(self, "z", float(self.z))

    def distance_to(self, other: "Point3D") -> float:
        """Return the Euclidean distance from this point to another point.

        Args:
            other: The target point.

        Returns:
            The straight-line distance between the two points.
        """
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return (dx * dx + dy * dy + dz * dz) ** 0.5

    def to_tuple(self) -> tuple[float, float, float]:
        """Return the point coordinates as a tuple."""
        return (self.x, self.y, self.z)

    def translated(self, dx: float, dy: float, dz: float) -> "Point3D":
        """Return a new point translated by the provided deltas.

        Args:
            dx: Translation along the x axis.
            dy: Translation along the y axis.
            dz: Translation along the z axis.

        Returns:
            A new Point3D instance with adjusted coordinates.
        """
        return Point3D(self.x + dx, self.y + dy, self.z + dz)

    def __eq__(self, other: object) -> bool:
        """Compare two points using the HGK precision policy.

        Args:
            other: Another object to compare.

        Returns:
            True when the two points are equal within tolerance.
        """
        if not isinstance(other, Point3D):
            return NotImplemented
        return self._precision_manager.compare_points(self.to_tuple(), other.to_tuple())

    def __hash__(self) -> int:
        """Return a hash based on the stored coordinates."""
        return hash(self.to_tuple())


__all__ = ["Point3D"]
