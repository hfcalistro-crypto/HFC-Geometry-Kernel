import pytest

from src.geometry.matrix3x3 import Matrix3x3
from src.geometry.vector3d import Vector3D


def test_identity_matrix_and_zero_matrix() -> None:
    identity = Matrix3x3.identity()
    zero = Matrix3x3.zero()

    assert identity.to_rows() == [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    assert zero.to_rows() == [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
    ]
    assert identity.is_identity()
    assert not zero.is_identity()


def test_from_rows_and_from_columns() -> None:
    rows = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0],
    ]
    columns = [
        [1.0, 4.0, 7.0],
        [2.0, 5.0, 8.0],
        [3.0, 6.0, 9.0],
    ]

    assert Matrix3x3.from_rows(rows).to_rows() == rows
    assert Matrix3x3.from_columns(columns).to_rows() == rows


def test_basic_arithmetic_operations() -> None:
    left = Matrix3x3.from_rows([[1.0, 2.0, 3.0], [0.0, 1.0, 4.0], [5.0, 6.0, 0.0]])
    right = Matrix3x3.from_rows([[1.0, 0.0, 1.0], [2.0, 1.0, 0.0], [0.0, 3.0, 1.0]])

    assert (left + right).to_rows() == [
        [2.0, 2.0, 4.0],
        [2.0, 2.0, 4.0],
        [5.0, 9.0, 1.0],
    ]
    assert (left - right).to_rows() == [
        [0.0, 2.0, 2.0],
        [-2.0, 0.0, 4.0],
        [5.0, 3.0, -1.0],
    ]
    assert (left * 2.0).to_rows() == [
        [2.0, 4.0, 6.0],
        [0.0, 2.0, 8.0],
        [10.0, 12.0, 0.0],
    ]
    assert (2.0 * left).to_rows() == [
        [2.0, 4.0, 6.0],
        [0.0, 2.0, 8.0],
        [10.0, 12.0, 0.0],
    ]


def test_matrix_multiplication_and_vector_application() -> None:
    left = Matrix3x3.from_rows([[1.0, 2.0, 0.0], [0.0, 1.0, 3.0], [4.0, 0.0, 1.0]])
    right = Matrix3x3.from_rows([[2.0, 0.0, 1.0], [1.0, 3.0, 0.0], [0.0, 1.0, 1.0]])
    vector = Vector3D(1.0, 2.0, 3.0)

    assert (left * right).to_rows() == [
        [4.0, 6.0, 1.0],
        [1.0, 6.0, 3.0],
        [8.0, 1.0, 5.0],
    ]
    assert (left * vector).to_tuple() == (5.0, 11.0, 7.0)


def test_determinant_transpose_and_inverse() -> None:
    matrix = Matrix3x3.from_rows([[1.0, 2.0, 3.0], [0.0, 1.0, 4.0], [5.0, 6.0, 0.0]])

    assert matrix.determinant() == 1.0
    assert matrix.transpose().to_rows() == [
        [1.0, 0.0, 5.0],
        [2.0, 1.0, 6.0],
        [3.0, 4.0, 0.0],
    ]
    assert matrix.inverse().to_rows() == [
        [-24.0, 18.0, 5.0],
        [20.0, -15.0, -4.0],
        [-5.0, 4.0, 1.0],
    ]


def test_cofactor_and_adjugate() -> None:
    matrix = Matrix3x3.from_rows([[1.0, 2.0, 3.0], [0.0, 1.0, 4.0], [5.0, 6.0, 0.0]])

    assert matrix.cofactor_matrix().to_rows() == [
        [-24.0, 20.0, -5.0],
        [18.0, -15.0, 4.0],
        [5.0, -4.0, 1.0],
    ]
    assert matrix.adjugate().to_rows() == [
        [-24.0, 18.0, 5.0],
        [20.0, -15.0, -4.0],
        [-5.0, 4.0, 1.0],
    ]


def test_is_orthogonal_for_rotation_like_matrix() -> None:
    matrix = Matrix3x3.from_rows([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])

    assert matrix.is_orthogonal()


def test_invalid_input_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Matrix3x3.from_rows([[1.0, 2.0], [3.0, 4.0]])

    with pytest.raises(ValueError):
        Matrix3x3.from_rows([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0, 10.0]])
