"""Immutable quaternion implementation for the HFC Geometry Kernel.

This module defines a lightweight, dependency-free quaternion type intended
for representing 3D rotations in a compact and immutable form. The initial
version focuses on the core algebra needed for composition, normalization,
and inversion.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .precision_manager import PrecisionManager


@dataclass(frozen=True)
class Quaternion:
    """Represent an immutable quaternion with scalar and vector components.

    The quaternion is stored as a tuple of four floating-point values in the
    form $(w, x, y, z)$, where $w$ is the real part and $(x, y, z)$ form the
    imaginary part. The class supports identity creation, length evaluation,
    normalization, conjugation, inversion, multiplication, and copying.
    """

    w: float
    x: float
    y: float
    z: float

    _precision_manager: PrecisionManager = PrecisionManager()

    def __post_init__(self) -> None:
        """Validate and normalize the quaternion components to floats."""
        for attribute_name, value in (("w", self.w), ("x", self.x), ("y", self.y), ("z", self.z)):
            if not isinstance(value, (int, float)):
                raise TypeError(f"{attribute_name} must be a real number")
        object.__setattr__(self, "w", float(self.w))
        object.__setattr__(self, "x", float(self.x))
        object.__setattr__(self, "y", float(self.y))
        object.__setattr__(self, "z", float(self.z))

    @classmethod
    def identity(cls) -> "Quaternion":
        """Return the identity quaternion."""
        return cls(1.0, 0.0, 0.0, 0.0)

    def length(self) -> float:
        """Return the Euclidean norm of the quaternion."""
        return math.sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self) -> "Quaternion":
        """Return a unit-length quaternion in the same direction.

        Raises:
            ValueError: If the quaternion has zero length.
        """
        magnitude = self.length()
        if self._precision_manager.compare_floats(magnitude, 0.0):
            raise ValueError("Cannot normalize a zero-length quaternion")
        return Quaternion(
            self.w / magnitude,
            self.x / magnitude,
            self.y / magnitude,
            self.z / magnitude,
        )

    def conjugate(self) -> "Quaternion":
        """Return the quaternion conjugate."""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self) -> "Quaternion":
        """Return the multiplicative inverse of the quaternion.

        Raises:
            ValueError: If the quaternion has zero length.
        """
        magnitude_squared = self.length() ** 2
        if self._precision_manager.compare_floats(magnitude_squared, 0.0):
            raise ValueError("Cannot invert a zero-length quaternion")
        return self.conjugate() * (1.0 / magnitude_squared)

    def multiply(self, other: object) -> "Quaternion":
        """Return the Hamilton product of this quaternion and another one.

        Args:
            other: Another quaternion instance.

        Raises:
            TypeError: If the supplied value is not a Quaternion.
        """
        if not isinstance(other, Quaternion):
            raise TypeError("other must be a Quaternion")

        return Quaternion(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def copy(self) -> "Quaternion":
        """Return a copy of this quaternion."""
        return Quaternion(self.w, self.x, self.y, self.z)

    def to_tuple(self) -> tuple[float, float, float, float]:
        """Return the quaternion components as a tuple."""
        return (self.w, self.x, self.y, self.z)

    def __mul__(self, other: object) -> "Quaternion":
        """Support quaternion multiplication or scalar scaling via the ``*`` operator."""
        if isinstance(other, Quaternion):
            return self.multiply(other)
        if isinstance(other, (int, float)):
            return Quaternion(
                self.w * float(other),
                self.x * float(other),
                self.y * float(other),
                self.z * float(other),
            )
        return NotImplemented

    def __rmul__(self, other: object) -> "Quaternion":
        """Support multiplication from the left with another quaternion or scalar."""
        if isinstance(other, Quaternion):
            return other.multiply(self)
        if isinstance(other, (int, float)):
            return self * other
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        """Compare two quaternions by their components."""
        if not isinstance(other, Quaternion):
            return NotImplemented
        return self.to_tuple() == other.to_tuple()


__all__ = ["Quaternion"]
