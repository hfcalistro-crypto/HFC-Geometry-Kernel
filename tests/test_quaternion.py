import math

import pytest

from src.geometry.quaternion import Quaternion


def test_quaternion_identity() -> None:
    quaternion = Quaternion.identity()

    assert quaternion == Quaternion(1.0, 0.0, 0.0, 0.0)
    assert quaternion.length() == 1.0


def test_quaternion_length_and_normalize() -> None:
    quaternion = Quaternion(3.0, 4.0, 0.0, 0.0)

    assert quaternion.length() == 5.0
    assert quaternion.normalize() == Quaternion(0.6, 0.8, 0.0, 0.0)


def test_quaternion_conjugate_and_inverse() -> None:
    quaternion = Quaternion(1.0, 2.0, 3.0, 4.0)

    assert quaternion.conjugate() == Quaternion(1.0, -2.0, -3.0, -4.0)
    assert quaternion.inverse() == Quaternion(0.03333333333333333, -0.06666666666666667, -0.1, -0.13333333333333333)


def test_quaternion_multiply_and_copy() -> None:
    left = Quaternion(1.0, 2.0, 3.0, 4.0)
    right = Quaternion(2.0, 3.0, 4.0, 5.0)

    assert left.multiply(right) == Quaternion(-36.0, 6.0, 12.0, 12.0)

    copy = left.copy()
    assert copy == left
    assert copy is not left


def test_quaternion_invalid_parameters() -> None:
    with pytest.raises(TypeError):
        Quaternion("1", 0.0, 0.0, 0.0)

    with pytest.raises(TypeError):
        Quaternion(1.0, 0.0, 0.0, 0.0).multiply("not-a-quaternion")

    with pytest.raises(ValueError):
        Quaternion(0.0, 0.0, 0.0, 0.0).normalize()

    with pytest.raises(ValueError):
        Quaternion(0.0, 0.0, 0.0, 0.0).inverse()
