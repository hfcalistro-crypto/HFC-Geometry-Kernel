import math

import pytest

from src.geometry.line3d import Line3D
from src.geometry.point3d import Point3D
from src.geometry.transform3d import Transform3D
from src.geometry.vector3d import Vector3D


def test_line3d_from_points_and_point_at() -> None:
    line = Line3D.from_points(Point3D(0.0, 0.0, 0.0), Point3D(2.0, 0.0, 0.0))

    assert line.point_at(0.0) == Point3D(0.0, 0.0, 0.0)
    assert line.point_at(2.0) == Point3D(2.0, 0.0, 0.0)


def test_line3d_contains_and_projection() -> None:
    line = Line3D.from_points(Point3D(0.0, 0.0, 0.0), Point3D(2.0, 0.0, 0.0))

    assert line.contains(Point3D(1.0, 0.0, 0.0)) is True
    assert line.contains(Point3D(1.0, 1.0, 0.0)) is False
    assert line.project_point(Point3D(1.0, 2.0, 0.0)) == Point3D(1.0, 0.0, 0.0)
    assert line.closest_point(Point3D(1.0, 2.0, 0.0)) == Point3D(1.0, 0.0, 0.0)
    assert line.distance_to_point(Point3D(1.0, 2.0, 0.0)) == 2.0


def test_line3d_parallel_and_perpendicular_and_angle() -> None:
    horizontal = Line3D.from_points(Point3D(0.0, 0.0, 0.0), Point3D(1.0, 0.0, 0.0))
    parallel = Line3D.from_points(Point3D(0.0, 1.0, 0.0), Point3D(2.0, 1.0, 0.0))
    vertical = Line3D.from_points(Point3D(0.0, 0.0, 0.0), Point3D(0.0, 1.0, 0.0))

    assert horizontal.parallel_to(parallel) is True
    assert horizontal.perpendicular_to(vertical) is True
    assert math.isclose(horizontal.angle_to(vertical), math.pi / 2.0)


def test_line3d_reverse_copy_and_transform() -> None:
    line = Line3D.from_points(Point3D(1.0, 1.0, 1.0), Point3D(2.0, 1.0, 1.0))

    reversed_line = line.reverse()
    assert reversed_line.direction == Vector3D(-1.0, 0.0, 0.0)
    assert reversed_line.origin == line.origin

    copied = line.copy()
    assert copied == line
    assert copied is not line

    translated = line.transform(Transform3D.translation(1.0, 2.0, 3.0))
    assert translated.origin == Point3D(2.0, 3.0, 4.0)
    assert translated.direction == Vector3D(1.0, 0.0, 0.0)


def test_line3d_invalid_inputs() -> None:
    with pytest.raises(TypeError):
        Line3D.from_points("invalid", Point3D(0.0, 0.0, 0.0))

    with pytest.raises(TypeError):
        Line3D.from_point_direction(Point3D(0.0, 0.0, 0.0), "invalid")

    with pytest.raises(ValueError):
        Line3D.from_points(Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0))

    with pytest.raises(ValueError):
        Line3D.from_point_direction(Point3D(0.0, 0.0, 0.0), Vector3D(0.0, 0.0, 0.0))

    with pytest.raises(TypeError):
        Line3D.from_points(Point3D(0.0, 0.0, 0.0), Point3D(1.0, 0.0, 0.0)).contains("invalid")

    with pytest.raises(TypeError):
        Line3D.from_points(Point3D(0.0, 0.0, 0.0), Point3D(1.0, 0.0, 0.0)).point_at("invalid")

    with pytest.raises(TypeError):
        Line3D.from_points(Point3D(0.0, 0.0, 0.0), Point3D(1.0, 0.0, 0.0)).parallel_to("invalid")
