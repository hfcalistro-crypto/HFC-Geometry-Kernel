from src.geometry.point3d import Point3D
from src.geometry.transform3d import Transform3D
from src.geometry.vector3d import Vector3D


def test_identity_transform_applies_no_change() -> None:
    transform = Transform3D.identity()

    point = transform.apply_to_point(Point3D(1.0, 2.0, 3.0))
    vector = transform.apply_to_vector(Vector3D(1.0, 2.0, 3.0))

    assert point.to_tuple() == (1.0, 2.0, 3.0)
    assert vector.to_tuple() == (1.0, 2.0, 3.0)


def test_translation_transform_moves_points_and_vectors() -> None:
    transform = Transform3D.translation(1.0, -2.0, 3.0)

    point = transform.apply_to_point(Point3D(1.0, 2.0, 3.0))
    vector = transform.apply_to_vector(Vector3D(1.0, 2.0, 3.0))

    assert point.to_tuple() == (2.0, 0.0, 6.0)
    assert vector.to_tuple() == (1.0, 2.0, 3.0)


def test_scale_transform_scales_components() -> None:
    transform = Transform3D.scale(2.0, 3.0, 4.0)

    point = transform.apply_to_point(Point3D(1.0, 2.0, 3.0))
    vector = transform.apply_to_vector(Vector3D(1.0, 2.0, 3.0))

    assert point.to_tuple() == (2.0, 6.0, 12.0)
    assert vector.to_tuple() == (2.0, 6.0, 12.0)


def test_rotation_z_transform_changes_coordinates() -> None:
    transform = Transform3D.rotation_z(3.141592653589793 / 2.0)

    point = transform.apply_to_point(Point3D(1.0, 0.0, 0.0))

    assert round(point.x, 6) == 0.0
    assert round(point.y, 6) == 1.0


def test_compose_and_matrix_export() -> None:
    first = Transform3D.translation(1.0, 0.0, 0.0)
    second = Transform3D.scale(2.0, 2.0, 2.0)
    composed = first.compose(second)

    matrix = composed.to_matrix()

    assert matrix.to_rows()[0][3] == 1.0
    assert matrix.to_rows()[1][1] == 2.0
