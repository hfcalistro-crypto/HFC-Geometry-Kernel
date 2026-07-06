"""Immutable 4x4 matrix implementation for the HFC Geometry Kernel.

This module provides a compact and dependency-free representation of a
4x4 transformation matrix that can be used by geometric components.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .point3d import Point3D
from .vector3d import Vector3D


@dataclass(frozen=True)
class Matrix4x4:
    """Represent an immutable 4x4 matrix of floating-point values.

    The matrix is stored as a tuple of four rows and supports identity
    creation, row-based construction, transpose, matrix multiplication,
    and transformation of Point3D and Vector3D instances.
    """

    rows: tuple[tuple[float, float, float, float], ...]

    def __post_init__(self) -> None:
        """Validate the matrix shape and normalize the stored values."""
        normalized_rows = self._normalize_rows(self.rows)
        object.__setattr__(self, "rows", normalized_rows)

    @staticmethod
    def _normalize_rows(rows: Sequence[Sequence[float]]) -> tuple[tuple[float, float, float, float], ...]:
        """Validate and normalize a 4x4 collection of rows."""
        if not isinstance(rows, (list, tuple)):
            raise TypeError("Matrix4x4 rows must be provided as a sequence")
        if len(rows) != 4:
            raise ValueError("Matrix4x4 must contain exactly 4 rows")

        normalized_rows: list[tuple[float, float, float, float]] = []
        for row_index, row in enumerate(rows):
            if not isinstance(row, (list, tuple)):
                raise TypeError(f"Row {row_index} must be a sequence")
            if len(row) != 4:
                raise ValueError(f"Row {row_index} must contain exactly 4 values")
            normalized_rows.append(tuple(float(component) for component in row))
        return tuple(normalized_rows)

    @classmethod
    def identity(cls) -> "Matrix4x4":
        """Return the identity matrix."""
        return cls.from_rows(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[float]]) -> "Matrix4x4":
        """Create a matrix from a 4x4 sequence of row vectors.

        Args:
            rows: A sequence containing exactly four rows, each with four values.

        Returns:
            A new immutable Matrix4x4 instance.

        Raises:
            TypeError: If the provided rows are not a sequence of sequences.
            ValueError: If the matrix does not contain exactly four rows or
                any row does not contain exactly four values.
        """
        return cls(tuple(rows))

    def to_rows(self) -> list[list[float]]:
        """Return the matrix as a list of rows."""
        return [list(row) for row in self.rows]

    def transpose(self) -> "Matrix4x4":
        """Return the transposed matrix."""
        return Matrix4x4.from_rows(
            [
                [self.rows[0][0], self.rows[1][0], self.rows[2][0], self.rows[3][0]],
                [self.rows[0][1], self.rows[1][1], self.rows[2][1], self.rows[3][1]],
                [self.rows[0][2], self.rows[1][2], self.rows[2][2], self.rows[3][2]],
                [self.rows[0][3], self.rows[1][3], self.rows[2][3], self.rows[3][3]],
            ]
        )

    def __mul__(self, other: object) -> object:
        """Multiply the matrix by another matrix or a geometric value."""
        if isinstance(other, Matrix4x4):
            return self._multiply_matrices(other)
        if isinstance(other, Point3D):
            return self._multiply_point(other)
        if isinstance(other, Vector3D):
            return self._multiply_vector(other)
        return NotImplemented

    def _multiply_matrices(self, other: "Matrix4x4") -> "Matrix4x4":
        """Multiply this matrix by another 4x4 matrix."""
        result_rows: list[list[float]] = []
        for row_index in range(4):
            result_row: list[float] = []
            for column_index in range(4):
                total = sum(
                    self.rows[row_index][k] * other.rows[k][column_index]
                    for k in range(4)
                )
                result_row.append(total)
            result_rows.append(result_row)
        return Matrix4x4.from_rows(result_rows)

    def _multiply_point(self, point: Point3D) -> Point3D:
        """Multiply the matrix by a Point3D instance."""
        x = (
            self.rows[0][0] * point.x
            + self.rows[0][1] * point.y
            + self.rows[0][2] * point.z
            + self.rows[0][3]
        )
        y = (
            self.rows[1][0] * point.x
            + self.rows[1][1] * point.y
            + self.rows[1][2] * point.z
            + self.rows[1][3]
        )
        z = (
            self.rows[2][0] * point.x
            + self.rows[2][1] * point.y
            + self.rows[2][2] * point.z
            + self.rows[2][3]
        )
        return Point3D(x, y, z)

    def _multiply_vector(self, vector: Vector3D) -> Vector3D:
        """Multiply the matrix by a Vector3D instance."""
        x = self.rows[0][0] * vector.x + self.rows[0][1] * vector.y + self.rows[0][2] * vector.z
        y = self.rows[1][0] * vector.x + self.rows[1][1] * vector.y + self.rows[1][2] * vector.z
        z = self.rows[2][0] * vector.x + self.rows[2][1] * vector.y + self.rows[2][2] * vector.z
        return Vector3D(x, y, z)


__all__ = ["Matrix4x4"]
