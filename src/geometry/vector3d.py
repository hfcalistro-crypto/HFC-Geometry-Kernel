"""Immutable 3D vector implementation for the HFC Geometry Kernel.

This module defines a lightweight, dependency-free vector type for
geometric operations and future HGK expansions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .precision_manager import PrecisionManager


@dataclass(frozen=True)
class Vector3D:
    """Represent an immutable 3D vector with floating-point components.

    The vector is stored in a compact immutable form and supports basic
    geometric operations such as length, normalization, dot and cross
    products, angle evaluation, scaling, and arithmetic composition.
    """

    x: float
    y: float
    z: float

    _precision_manager: PrecisionManager = PrecisionManager()

    def __post_init__(self) -> None:
        """Normalize the stored components to floating-point values."""
        object.__setattr__(self, "x", float(self.x))
        object.__setattr__(self, "y", float(self.y))
        object.__setattr__(self, "z", float(self.z))

    def length(self) -> float:
        """Return the Euclidean length of the vector."""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalized(self) -> "Vector3D":
        """Return a unit-length vector in the same direction.

        Raises:
            ValueError: If the vector is zero-length.
        """
        magnitude = self.length()
        if self._precision_manager.compare_floats(magnitude, 0.0):
            raise ValueError("Cannot normalize a zero-length vector")
        return Vector3D(self.x / magnitude, self.y / magnitude, self.z / magnitude)

    def dot(self, other: "Vector3D") -> float:
        """Return the dot product with another vector."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3D") -> "Vector3D":
        """Return the cross product with another vector."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def angle_to(self, other: "Vector3D") -> float:
        """Return the angle between this vector and another vector in radians.

        Raises:
            ValueError: If either vector is zero-length.
        """
        if self._precision_manager.compare_floats(self.length(), 0.0):
            raise ValueError("Cannot compute angle with a zero-length vector")
        if self._precision_manager.compare_floats(other.length(), 0.0):
            raise ValueError("Cannot compute angle with a zero-length vector")

        cosine = self.dot(other) / (self.length() * other.length())
        cosine = max(-1.0, min(1.0, cosine))
        return math.acos(cosine)

    def to_tuple(self) -> tuple[float, float, float]:
        """Return the vector components as a tuple."""
        return (self.x, self.y, self.z)

    def scaled(self, factor: float) -> "Vector3D":
        """Return a vector scaled by the provided factor."""
        return Vector3D(self.x * factor, self.y * factor, self.z * factor)

    def __add__(self, other: "Vector3D") -> "Vector3D":
        """Return the sum of two vectors."""
        if not isinstance(other, Vector3D):
            return NotImplemented
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3D") -> "Vector3D":
        """Return the difference of two vectors."""
        if not isinstance(other, Vector3D):
            return NotImplemented
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, factor: float) -> "Vector3D":
        """Return a vector multiplied by a scalar."""
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return self.scaled(float(factor))

    def __truediv__(self, factor: float) -> "Vector3D":
        """Return a vector divided by a scalar."""
        if not isinstance(factor, (int, float)):
            return NotImplemented
        if self._precision_manager.compare_floats(float(factor), 0.0):
            raise ZeroDivisionError("Cannot divide a vector by zero")
        return Vector3D(self.x / factor, self.y / factor, self.z / factor)

    def __eq__(self, other: object) -> bool:
        """Compare two vectors using the HGK precision policy."""
        if not isinstance(other, Vector3D):
            return NotImplemented
        return self._precision_manager.compare_vectors(self.to_tuple(), other.to_tuple())

    def __hash__(self) -> int:
        """Return a hash based on the stored components."""
        return hash(self.to_tuple())


__all__ = ["Vector3D"]
