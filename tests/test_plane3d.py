import math

import pytest

from src.geometry.line3d import Line3D
from src.geometry.plane3d import Plane3D
from src.geometry.point3d import Point3D
from src.geometry.transform3d import Transform3D
from src.geometry.vector3d import Vector3D


def test_plane3d_creation_and_constructors() -> None:
    plane = Plane3D.from_point_normal(Point3D(1.0, 2.0, 3.0), Vector3D(0.0, 0.0, 2.0))

    assert plane.point == Point3D(1.0, 2.0, 3.0)
    assert plane.normal == Vector3D(0.0, 0.0, 1.0)

    from_points = Plane3D.from_points(
        Point3D(0.0, 0.0, 0.0),
        Point3D(1.0, 0.0, 0.0),
        Point3D(0.0, 1.0, 0.0),
    )
    assert from_points.normal == Vector3D(0.0, 0.0, 1.0)

    from_equation = Plane3D.from_equation(0.0, 0.0, 1.0, 0.0)
    assert from_equation == from_points


def test_plane3d_normalization_distances_and_projection() -> None:
    plane = Plane3D.from_point_normal(Point3D(0.0, 0.0, 0.0), Vector3D(0.0, 0.0, 2.0))

    assert plane.normal == Vector3D(0.0, 0.0, 1.0)
    assert plane.signed_distance(Point3D(0.0, 0.0, 2.0)) == 2.0
    assert plane.distance_to_point(Point3D(0.0, 0.0, 2.0)) == 2.0
    assert plane.contains(Point3D(1.0, 2.0, 0.0)) is True
    assert plane.contains(Point3D(1.0, 2.0, 1.0)) is False
    assert plane.project_point(Point3D(1.0, 2.0, 3.0)) == Point3D(1.0, 2.0, 0.0)
    assert plane.closest_point(Point3D(1.0, 2.0, 3.0)) == Point3D(1.0, 2.0, 0.0)


def test_plane3d_intersection_and_angles() -> None:
    plane = Plane3D.from_point_normal(Point3D(0.0, 0.0, 0.0), Vector3D(0.0, 0.0, 1.0))
    line = Line3D.from_points(Point3D(0.0, 0.0, 1.0), Point3D(0.0, 0.0, -1.0))
    parallel_line = Line3D.from_points(Point3D(1.0, 1.0, 1.0), Point3D(2.0, 2.0, 1.0))
    line_in_plane = Line3D.from_points(Point3D(0.0, 0.0, 0.0), Point3D(1.0, 0.0, 0.0))
    vertical_line = Line3D.from_points(Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 1.0))
    orthogonal_plane = Plane3D.from_point_normal(Point3D(0.0, 0.0, 0.0), Vector3D(1.0, 0.0, 0.0))

    assert plane.intersect_line(line) == Point3D(0.0, 0.0, 0.0)
    assert plane.intersect_line(parallel_line) is None
    assert math.isclose(plane.angle_to_line(line_in_plane), 0.0)
    assert math.isclose(plane.angle_to_line(vertical_line), math.pi / 2.0)
    assert math.isclose(plane.angle_to_plane(orthogonal_plane), math.pi / 2.0)


def test_plane3d_transform_copy_and_normalize() -> None:
    plane = Plane3D.from_point_normal(Point3D(0.0, 0.0, 0.0), Vector3D(0.0, 0.0, 1.0))

    transformed = plane.transform(Transform3D.translation(1.0, 2.0, 3.0))
    assert transformed.point == Point3D(1.0, 2.0, 3.0)
    assert transformed.normal == Vector3D(0.0, 0.0, 1.0)

    copied = plane.copy()
    assert copied == plane
    assert copied is not plane

    normalized = plane.normalize()
    assert normalized is plane


def test_plane3d_invalid_inputs() -> None:
    with pytest.raises(TypeError):
        Plane3D.from_point_normal("invalid", Vector3D(0.0, 0.0, 1.0))

    with pytest.raises(TypeError):
        Plane3D.from_point_normal(Point3D(0.0, 0.0, 0.0), "invalid")

    with pytest.raises(ValueError):
        Plane3D.from_point_normal(Point3D(0.0, 0.0, 0.0), Vector3D(0.0, 0.0, 0.0))

    with pytest.raises(ValueError):
        Plane3D.from_points(
            Point3D(0.0, 0.0, 0.0),
            Point3D(1.0, 0.0, 0.0),
            Point3D(2.0, 0.0, 0.0),
        )

    plane = Plane3D.from_point_normal(Point3D(0.0, 0.0, 0.0), Vector3D(0.0, 0.0, 1.0))

    with pytest.raises(TypeError):
        plane.contains("invalid")

    with pytest.raises(TypeError):
        plane.intersect_line("invalid")

    with pytest.raises(TypeError):
        plane.angle_to_plane("invalid")
