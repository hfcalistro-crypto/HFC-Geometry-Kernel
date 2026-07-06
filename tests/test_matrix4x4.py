import pytest

from src.geometry.matrix4x4 import Matrix4x4
from src.geometry.point3d import Point3D
from src.geometry.vector3d import Vector3D


def test_identity_matrix_and_rows() -> None:
    matrix = Matrix4x4.identity()

    assert matrix.to_rows() == [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def test_from_rows_and_transpose() -> None:
    matrix = Matrix4x4.from_rows(
        [
            [1.0, 2.0, 3.0, 4.0],
            [5.0, 6.0, 7.0, 8.0],
            [9.0, 10.0, 11.0, 12.0],
            [13.0, 14.0, 15.0, 16.0],
        ]
    )

    assert matrix.to_rows()[0][1] == 2.0
    assert matrix.transpose().to_rows()[1][0] == 2.0


def test_matrix_multiplication() -> None:
    left = Matrix4x4.from_rows(
        [
            [1.0, 2.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )
    right = Matrix4x4.from_rows(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    assert (left * right).to_rows()[0][0] == 1.0


def test_matrix_multiplies_point3d() -> None:
    matrix = Matrix4x4.from_rows(
        [
            [1.0, 0.0, 0.0, 2.0],
            [0.0, 1.0, 0.0, 3.0],
            [0.0, 0.0, 1.0, 4.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )
    point = Point3D(1.0, 2.0, 3.0)

    transformed = matrix * point
    assert transformed.to_tuple() == (3.0, 5.0, 7.0)


def test_matrix_multiplies_vector3d() -> None:
    matrix = Matrix4x4.from_rows(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 2.0, 0.0, 0.0],
            [0.0, 0.0, 3.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )
    vector = Vector3D(1.0, 2.0, 3.0)

    transformed = matrix * vector
    assert transformed.to_tuple() == (1.0, 4.0, 9.0)


def test_invalid_matrix_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Matrix4x4.from_rows(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 0.0, 0.0],
            ]
        )
