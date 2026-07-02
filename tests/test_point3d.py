from src.geometry.point3d import Point3D


def test_point3d_is_immutable() -> None:
    point = Point3D(1.0, 2.0, 3.0)

    try:
        point.x = 4.0
    except AttributeError:
        pass
    else:
        raise AssertionError("Point3D should be immutable")


def test_point3d_distance_to_computes_euclidean_distance() -> None:
    point_a = Point3D(0.0, 0.0, 0.0)
    point_b = Point3D(3.0, 4.0, 0.0)

    assert point_a.distance_to(point_b) == 5.0


def test_point3d_to_tuple_returns_coordinates() -> None:
    point = Point3D(1.5, -2.0, 3.25)

    assert point.to_tuple() == (1.5, -2.0, 3.25)


def test_point3d_translated_returns_new_instance() -> None:
    point = Point3D(1.0, 2.0, 3.0)
    translated = point.translated(1.0, -1.0, 2.0)

    assert translated is not point
    assert translated.to_tuple() == (2.0, 1.0, 5.0)
    assert point.to_tuple() == (1.0, 2.0, 3.0)


def test_point3d_equality_uses_precision_manager() -> None:
    point_a = Point3D(0.0, 0.0, 0.0)
    point_b = Point3D(1e-7, 0.0, 0.0)
    point_c = Point3D(2e-6, 0.0, 0.0)

    assert point_a == point_b
    assert point_a != point_c
