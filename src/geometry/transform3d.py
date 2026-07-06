"""Immutable 3D transformation implementation for the HFC Geometry Kernel.

This module provides a lightweight transformation wrapper over a 4x4
matrix so that Point3D and Vector3D instances can be transformed in a
consistent and extensible way.
"""

from __future__ import annotations

from dataclasses import dataclass

from .matrix4x4 import Matrix4x4
from .point3d import Point3D
from .vector3d import Vector3D


@dataclass(frozen=True)
class Transform3D:
    """Represent an immutable 3D transformation using a 4x4 matrix.

    The class exposes high-level constructors for the basic affine
    transformations used by the HGK geometry primitives.
    """

    matrix: Matrix4x4

    @classmethod
    def identity(cls) -> "Transform3D":
        """Return an identity transformation."""
        return cls(Matrix4x4.identity())

    @classmethod
    def translation(cls, tx: float, ty: float, tz: float) -> "Transform3D":
        """Return a translation transformation.

        Args:
            tx: Translation along the x axis.
            ty: Translation along the y axis.
            tz: Translation along the z axis.

        Returns:
            A transformation that translates points by the provided offsets.

        Raises:
            TypeError: If any argument is not a real number.
        """
        cls._validate_scalar(tx, "tx")
        cls._validate_scalar(ty, "ty")
        cls._validate_scalar(tz, "tz")
        return cls(
            Matrix4x4.from_rows(
                [
                    [1.0, 0.0, 0.0, float(tx)],
                    [0.0, 1.0, 0.0, float(ty)],
                    [0.0, 0.0, 1.0, float(tz)],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            )
        )

    @classmethod
    def scale(cls, sx: float, sy: float, sz: float) -> "Transform3D":
        """Return a scaling transformation.

        Args:
            sx: Scale factor along the x axis.
            sy: Scale factor along the y axis.
            sz: Scale factor along the z axis.

        Returns:
            A transformation that scales points and vectors.

        Raises:
            TypeError: If any argument is not a real number.
        """
        cls._validate_scalar(sx, "sx")
        cls._validate_scalar(sy, "sy")
        cls._validate_scalar(sz, "sz")
        return cls(
            Matrix4x4.from_rows(
                [
                    [float(sx), 0.0, 0.0, 0.0],
                    [0.0, float(sy), 0.0, 0.0],
                    [0.0, 0.0, float(sz), 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            )
        )

    def apply_to_point(self, point: Point3D) -> Point3D:
        """Apply the transformation to a Point3D instance."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")
        return self.matrix * point

    def apply_to_vector(self, vector: Vector3D) -> Vector3D:
        """Apply the transformation to a Vector3D instance."""
        if not isinstance(vector, Vector3D):
            raise TypeError("vector must be a Vector3D")
        return self.matrix * vector

    def to_matrix(self) -> Matrix4x4:
        """Return the underlying 4x4 matrix used by this transform."""
        return self.matrix

    @staticmethod
    def _validate_scalar(value: object, name: str) -> None:
        """Validate that a value is a real scalar."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a real number")


__all__ = ["Transform3D"]
