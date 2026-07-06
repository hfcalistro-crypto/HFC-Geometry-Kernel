import pytest

from src.geometry.point3d import Point3D
from src.geometry.transform3d import Transform3D
from src.geometry.vector3d import Vector3D


def test_identity_transform_applies_no_change() -> None:
    transform = Transform3D.identity()

    point = transform.apply_to_point(Point3D(1.0, 2.0, 3.0))
    vector = transform.apply_to_vector(Vector3D(1.0, 2.0, 3.0))

    assert point.to_tuple() == (1.0, 2.0, 3.0)
    assert vector.to_tuple() == (1.0, 2.0, 3.0)


def test_translation_moves_points() -> None:
    transform = Transform3D.translation(1.0, -2.0, 3.0)

    point = transform.apply_to_point(Point3D(1.0, 2.0, 3.0))

    assert point.to_tuple() == (2.0, 0.0, 6.0)


def test_scale_moves_points() -> None:
    transform = Transform3D.scale(2.0, 3.0, 4.0)

    point = transform.apply_to_point(Point3D(1.0, 2.0, 3.0))

    assert point.to_tuple() == (2.0, 6.0, 12.0)


def test_transform_applies_to_vector() -> None:
    transform = Transform3D.scale(2.0, 2.0, 2.0)
    vector = transform.apply_to_vector(Vector3D(1.0, 2.0, 3.0))

    assert vector.to_tuple() == (2.0, 4.0, 6.0)


def test_invalid_parameters_raise_type_error() -> None:
    with pytest.raises(TypeError):
        Transform3D.translation("1", 0.0, 0.0)

    with pytest.raises(TypeError):
        Transform3D.scale(1.0, None, 1.0)

    with pytest.raises(TypeError):
        Transform3D.identity().apply_to_point("not-a-point")

    with pytest.raises(TypeError):
        Transform3D.identity().apply_to_vector("not-a-vector")
