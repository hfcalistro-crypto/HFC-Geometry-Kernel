"""Immutable 3x3 matrix implementation for the HFC Geometry Kernel.

This module provides a compact and dependency-free representation of a
3x3 matrix that supports common linear algebra operations used by the
HGK geometry primitives.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .vector3d import Vector3D


@dataclass(frozen=True)
class Matrix3x3:
    """Represent an immutable 3x3 matrix of floating-point values.

    The matrix is stored as a tuple of three rows and supports construction
    from rows or columns, scalar and matrix arithmetic, determinant,
    transpose, inverse, adjugate, cofactor extraction, and vector application.
    """

    rows: tuple[tuple[float, float, float], ...]

    def __post_init__(self) -> None:
        """Validate and normalize the matrix data."""
        normalized_rows = self._normalize_rows(self.rows)
        object.__setattr__(self, "rows", normalized_rows)

    @staticmethod
    def _normalize_rows(rows: Sequence[Sequence[float]]) -> tuple[tuple[float, float, float], ...]:
        """Validate and normalize a 3x3 collection of rows."""
        if not isinstance(rows, (list, tuple)):
            raise TypeError("Matrix3x3 rows must be provided as a sequence")
        if len(rows) != 3:
            raise ValueError("Matrix3x3 must contain exactly 3 rows")

        normalized_rows: list[tuple[float, float, float]] = []
        for row_index, row in enumerate(rows):
            if not isinstance(row, (list, tuple)):
                raise TypeError(f"Row {row_index} must be a sequence")
            if len(row) != 3:
                raise ValueError(f"Row {row_index} must contain exactly 3 values")
            normalized_rows.append(tuple(float(component) for component in row))
        return tuple(normalized_rows)

    @classmethod
    def identity(cls) -> "Matrix3x3":
        """Return the 3x3 identity matrix."""
        return cls.from_rows(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        )

    @classmethod
    def zero(cls) -> "Matrix3x3":
        """Return the 3x3 zero matrix."""
        return cls.from_rows(
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        )

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[float]]) -> "Matrix3x3":
        """Create a matrix from three row vectors."""
        return cls(tuple(rows))

    @classmethod
    def from_columns(cls, columns: Sequence[Sequence[float]]) -> "Matrix3x3":
        """Create a matrix from three column vectors."""
        if len(columns) != 3:
            raise ValueError("Matrix3x3 must contain exactly 3 columns")

        normalized_columns: list[list[float]] = []
        for column_index, column in enumerate(columns):
            if not isinstance(column, (list, tuple)):
                raise TypeError(f"Column {column_index} must be a sequence")
            if len(column) != 3:
                raise ValueError(f"Column {column_index} must contain exactly 3 values")
            normalized_columns.append([float(value) for value in column])

        rows: list[list[float]] = []
        for row_index in range(3):
            rows.append([normalized_columns[column_index][row_index] for column_index in range(3)])
        return cls.from_rows(rows)

    def copy(self) -> "Matrix3x3":
        """Return a copy of this matrix."""
        return Matrix3x3.from_rows(self.to_rows())

    def to_rows(self) -> list[list[float]]:
        """Return the matrix as a list of rows."""
        return [list(row) for row in self.rows]

    def to_tuple(self) -> tuple[tuple[float, float, float], ...]:
        """Return the matrix as an immutable tuple of rows."""
        return self.rows

    def transpose(self) -> "Matrix3x3":
        """Return the transpose of the matrix."""
        return Matrix3x3.from_rows(
            [
                [self.rows[0][0], self.rows[1][0], self.rows[2][0]],
                [self.rows[0][1], self.rows[1][1], self.rows[2][1]],
                [self.rows[0][2], self.rows[1][2], self.rows[2][2]],
            ]
        )

    def determinant(self) -> float:
        """Return the determinant of the matrix."""
        return (
            self.rows[0][0] * (self.rows[1][1] * self.rows[2][2] - self.rows[1][2] * self.rows[2][1])
            - self.rows[0][1] * (self.rows[1][0] * self.rows[2][2] - self.rows[1][2] * self.rows[2][0])
            + self.rows[0][2] * (self.rows[1][0] * self.rows[2][1] - self.rows[1][1] * self.rows[2][0])
        )

    def cofactor_matrix(self) -> "Matrix3x3":
        """Return the matrix of cofactors for this matrix."""
        return Matrix3x3.from_rows(
            [
                [
                    +(self.rows[1][1] * self.rows[2][2] - self.rows[1][2] * self.rows[2][1]),
                    -(self.rows[1][0] * self.rows[2][2] - self.rows[1][2] * self.rows[2][0]),
                    +(self.rows[1][0] * self.rows[2][1] - self.rows[1][1] * self.rows[2][0]),
                ],
                [
                    -(self.rows[0][1] * self.rows[2][2] - self.rows[0][2] * self.rows[2][1]),
                    +(self.rows[0][0] * self.rows[2][2] - self.rows[0][2] * self.rows[2][0]),
                    -(self.rows[0][0] * self.rows[2][1] - self.rows[0][1] * self.rows[2][0]),
                ],
                [
                    +(self.rows[0][1] * self.rows[1][2] - self.rows[0][2] * self.rows[1][1]),
                    -(self.rows[0][0] * self.rows[1][2] - self.rows[0][2] * self.rows[1][0]),
                    +(self.rows[0][0] * self.rows[1][1] - self.rows[0][1] * self.rows[1][0]),
                ],
            ]
        )

    def adjugate(self) -> "Matrix3x3":
        """Return the adjugate (classical adjoint) of the matrix."""
        return self.cofactor_matrix().transpose()

    def inverse(self) -> "Matrix3x3":
        """Return the inverse of the matrix.

        Raises:
            ValueError: If the matrix is singular and therefore not invertible.
        """
        determinant = self.determinant()
        if abs(determinant) < 1e-12:
            raise ValueError("Matrix3x3 is singular and cannot be inverted")
        return self.adjugate() * (1.0 / determinant)

    def is_identity(self) -> bool:
        """Return True when the matrix is the identity matrix."""
        return self == Matrix3x3.identity()

    def is_orthogonal(self) -> bool:
        """Return True when the matrix is orthogonal.

        A matrix is orthogonal when its transpose is its inverse.
        """
        if abs(self.determinant()) < 1e-12:
            return False
        return self.transpose() == self.inverse()

    def __add__(self, other: object) -> object:
        """Return the sum of two matrices."""
        if not isinstance(other, Matrix3x3):
            return NotImplemented
        return Matrix3x3.from_rows(
            [
                [self.rows[0][0] + other.rows[0][0], self.rows[0][1] + other.rows[0][1], self.rows[0][2] + other.rows[0][2]],
                [self.rows[1][0] + other.rows[1][0], self.rows[1][1] + other.rows[1][1], self.rows[1][2] + other.rows[1][2]],
                [self.rows[2][0] + other.rows[2][0], self.rows[2][1] + other.rows[2][1], self.rows[2][2] + other.rows[2][2]],
            ]
        )

    def __sub__(self, other: object) -> object:
        """Return the difference of two matrices."""
        if not isinstance(other, Matrix3x3):
            return NotImplemented
        return Matrix3x3.from_rows(
            [
                [self.rows[0][0] - other.rows[0][0], self.rows[0][1] - other.rows[0][1], self.rows[0][2] - other.rows[0][2]],
                [self.rows[1][0] - other.rows[1][0], self.rows[1][1] - other.rows[1][1], self.rows[1][2] - other.rows[1][2]],
                [self.rows[2][0] - other.rows[2][0], self.rows[2][1] - other.rows[2][1], self.rows[2][2] - other.rows[2][2]],
            ]
        )

    def __mul__(self, other: object) -> object:
        """Multiply the matrix by another matrix, a vector, or a scalar."""
        if isinstance(other, Matrix3x3):
            return self._multiply_matrices(other)
        if isinstance(other, Vector3D):
            return self._multiply_vector(other)
        if isinstance(other, (int, float)):
            return self._multiply_scalar(float(other))
        return NotImplemented

    def __rmul__(self, other: object) -> object:
        """Support scalar multiplication from the left."""
        return self.__mul__(other)

    def _multiply_matrices(self, other: "Matrix3x3") -> "Matrix3x3":
        """Multiply this matrix by another 3x3 matrix."""
        result_rows: list[list[float]] = []
        for row_index in range(3):
            result_row: list[float] = []
            for column_index in range(3):
                value = sum(
                    self.rows[row_index][k] * other.rows[k][column_index]
                    for k in range(3)
                )
                result_row.append(value)
            result_rows.append(result_row)
        return Matrix3x3.from_rows(result_rows)

    def _multiply_vector(self, vector: Vector3D) -> Vector3D:
        """Multiply this matrix by a Vector3D."""
        x = self.rows[0][0] * vector.x + self.rows[0][1] * vector.y + self.rows[0][2] * vector.z
        y = self.rows[1][0] * vector.x + self.rows[1][1] * vector.y + self.rows[1][2] * vector.z
        z = self.rows[2][0] * vector.x + self.rows[2][1] * vector.y + self.rows[2][2] * vector.z
        return Vector3D(x, y, z)

    def _multiply_scalar(self, scalar: float) -> "Matrix3x3":
        """Multiply this matrix by a scalar value."""
        return Matrix3x3.from_rows(
            [
                [self.rows[0][0] * scalar, self.rows[0][1] * scalar, self.rows[0][2] * scalar],
                [self.rows[1][0] * scalar, self.rows[1][1] * scalar, self.rows[1][2] * scalar],
                [self.rows[2][0] * scalar, self.rows[2][1] * scalar, self.rows[2][2] * scalar],
            ]
        )

    def __eq__(self, other: object) -> bool:
        """Compare two matrices using exact floating-point equality."""
        if not isinstance(other, Matrix3x3):
            return NotImplemented
        return self.rows == other.rows


__all__ = ["Matrix3x3"]
