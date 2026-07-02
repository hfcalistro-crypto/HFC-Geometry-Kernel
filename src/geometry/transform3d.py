"""Immutable 3D transformation implementation for the HFC Geometry Kernel.

This module provides a lightweight transformation wrapper over a 4x4
matrix so that Point3D and Vector3D instances can be transformed in a
consistent and extensible way.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .matrix4x4 import Matrix4x4
from .point3d import Point3D
from .vector3d import Vector3D


@dataclass(frozen=True)
class Transform3D:
    """Represent an immutable 3D transformation using a 4x4 matrix.

    The class exposes high-level constructors for common transformations
    such as translation, scaling, and rotations around the coordinate axes.
    It is designed to be simple, dependency-free, and compatible with the
    point and vector primitives defined by the HGK.
    """

    matrix: Matrix4x4

    @classmethod
    def identity(cls) -> "Transform3D":
        """Return an identity transformation."""
        return cls(Matrix4x4.identity())

    @classmethod
    def translation(cls, dx: float, dy: float, dz: float) -> "Transform3D":
        """Return a translation transformation."""
        return cls(
            Matrix4x4.from_rows(
                [
                    [1.0, 0.0, 0.0, dx],
                    [0.0, 1.0, 0.0, dy],
                    [0.0, 0.0, 1.0, dz],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            )
        )

    @classmethod
    def scale(cls, sx: float, sy: float, sz: float) -> "Transform3D":
        """Return a scaling transformation."""
        return cls(
            Matrix4x4.from_rows(
                [
                    [sx, 0.0, 0.0, 0.0],
                    [0.0, sy, 0.0, 0.0],
                    [0.0, 0.0, sz, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            )
        )

    @classmethod
    def rotation_x(cls, angle_radians: float) -> "Transform3D":
        """Return a rotation around the X axis."""
        cosine = math.cos(angle_radians)
        sine = math.sin(angle_radians)
        return cls(
            Matrix4x4.from_rows(
                [
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, cosine, -sine, 0.0],
                    [0.0, sine, cosine, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            )
        )

    @classmethod
    def rotation_y(cls, angle_radians: float) -> "Transform3D":
        """Return a rotation around the Y axis."""
        cosine = math.cos(angle_radians)
        sine = math.sin(angle_radians)
        return cls(
            Matrix4x4.from_rows(
                [
                    [cosine, 0.0, sine, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [-sine, 0.0, cosine, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            )
        )

    @classmethod
    def rotation_z(cls, angle_radians: float) -> "Transform3D":
        """Return a rotation around the Z axis."""
        cosine = math.cos(angle_radians)
        sine = math.sin(angle_radians)
        return cls(
            Matrix4x4.from_rows(
                [
                    [cosine, -sine, 0.0, 0.0],
                    [sine, cosine, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            )
        )

    def apply_to_point(self, point: Point3D) -> Point3D:
        """Apply the transformation to a Point3D instance."""
        return self.matrix * point

    def apply_to_vector(self, vector: Vector3D) -> Vector3D:
        """Apply the transformation to a Vector3D instance."""
        return self.matrix * vector

    def compose(self, other: "Transform3D") -> "Transform3D":
        """Return a new transformation that applies this transform after another."""
        return Transform3D(self.matrix * other.matrix)

    def to_matrix(self) -> Matrix4x4:
        """Return the underlying 4x4 matrix."""
        return self.matrix


__all__ = ["Transform3D"]
