import math

import pytest

from src.geometry.vector3d import Vector3D


def test_vector3d_is_immutable() -> None:
    vector = Vector3D(1.0, 2.0, 3.0)

    try:
        vector.x = 4.0
    except AttributeError:
        pass
    else:
        raise AssertionError("Vector3D should be immutable")


def test_vector3d_length_and_normalized() -> None:
    vector = Vector3D(3.0, 4.0, 0.0)

    assert vector.length() == 5.0
    assert vector.normalized().to_tuple() == (0.6, 0.8, 0.0)


def test_vector3d_dot_and_cross_products() -> None:
    left = Vector3D(1.0, 2.0, 3.0)
    right = Vector3D(4.0, 5.0, 6.0)

    assert left.dot(right) == 32.0
    assert left.cross(right).to_tuple() == (-3.0, 6.0, -3.0)


def test_vector3d_angle_to() -> None:
    left = Vector3D(1.0, 0.0, 0.0)
    right = Vector3D(0.0, 1.0, 0.0)

    assert math.isclose(left.angle_to(right), math.pi / 2.0)


def test_vector3d_scaling_and_arithmetic() -> None:
    vector = Vector3D(1.0, 2.0, 3.0)

    assert vector.scaled(2.0).to_tuple() == (2.0, 4.0, 6.0)
    assert (vector + Vector3D(1.0, 1.0, 1.0)).to_tuple() == (2.0, 3.0, 4.0)
    assert (vector - Vector3D(1.0, 1.0, 1.0)).to_tuple() == (0.0, 1.0, 2.0)
    assert (vector * 2.0).to_tuple() == (2.0, 4.0, 6.0)
    assert (vector / 2.0).to_tuple() == (0.5, 1.0, 1.5)


def test_vector3d_equality_and_zero_validation() -> None:
    vector_a = Vector3D(0.0, 0.0, 0.0)
    vector_b = Vector3D(1e-7, 0.0, 0.0)
    vector_c = Vector3D(2e-6, 0.0, 0.0)

    assert vector_a == vector_b
    assert vector_a != vector_c

    with pytest.raises(ValueError):
        Vector3D(0.0, 0.0, 0.0).normalized()

    with pytest.raises(ValueError):
        Vector3D(1.0, 0.0, 0.0).angle_to(Vector3D(0.0, 0.0, 0.0))
