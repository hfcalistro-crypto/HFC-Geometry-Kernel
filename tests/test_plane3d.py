import math

from src.geometry.matrix4x4 import Matrix4x4
from src.geometry.point3d import Point3D
from src.geometry.plane3d import Plane3D
from src.geometry.transform3d import Transform3D
from src.geometry.vector3d import Vector3D


def test_plane3d_from_points_and_coefficients() -> None:
    p1 = Point3D(0.0, 0.0, 0.0)
    p2 = Point3D(1.0, 0.0, 0.0)
    p3 = Point3D(0.0, 1.0, 0.0)

    plane = Plane3D.from_points(p1, p2, p3)
    assert plane.normal == Vector3D(0.0, 0.0, 1.0)
    assert plane.is_point_on_plane(Point3D(0.5, 0.5, 0.0))

    plane_from_coeffs = Plane3D.from_coefficients(0.0, 0.0, 2.0, 0.0)
    assert plane_from_coeffs.normal == Vector3D(0.0, 0.0, 1.0)
    assert plane_from_coeffs.is_point_on_plane(Point3D(0.1, 0.1, 0.0))


def test_plane3d_normal_and_signed_distance() -> None:
    plane = Plane3D.from_coefficients(0.0, 0.0, 1.0, -2.0)
    assert plane.normal == Vector3D(0.0, 0.0, 1.0)
    assert plane.signed_distance_to_point(Point3D(0.0, 0.0, 3.0)) == 1.0
    assert plane.distance_to_point(Point3D(0.0, 0.0, 3.0)) == 1.0


def test_plane3d_projection() -> None:
    plane = Plane3D.from_coefficients(0.0, 0.0, 1.0, 0.0)
    point = Point3D(1.0, 2.0, 3.0)
    projected = plane.project_point(point)

    assert projected == Point3D(1.0, 2.0, 0.0)
    assert plane.is_point_on_plane(projected)


def test_plane3d_parallel_and_orthogonal() -> None:
    base_plane = Plane3D.from_coefficients(0.0, 0.0, 1.0, 0.0)
    parallel_plane = Plane3D.from_coefficients(0.0, 0.0, 2.0, -5.0)
    orthogonal_plane = Plane3D.from_coefficients(1.0, 0.0, 0.0, -1.0)

    assert base_plane.is_parallel_to(parallel_plane)
    assert not base_plane.is_orthogonal_to(parallel_plane)
    assert base_plane.is_orthogonal_to(orthogonal_plane)
    assert not base_plane.is_parallel_to(orthogonal_plane)


def test_plane3d_apply_transform_and_matrix() -> None:
    plane = Plane3D.from_coefficients(0.0, 0.0, 1.0, -1.0)
    transform = Transform3D.translation(0.0, 0.0, 2.0)
    transformed_plane = plane.apply_transform(transform)

    assert transformed_plane.is_point_on_plane(Point3D(0.0, 0.0, 3.0))
    assert transformed_plane.normal == plane.normal

    matrix = Matrix4x4.from_rows(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )
    matrix_transformed_plane = plane.apply_matrix(matrix)
    assert matrix_transformed_plane.is_point_on_plane(Point3D(0.0, 0.0, 2.0))
    assert matrix_transformed_plane.normal == plane.normal


def test_plane3d_equality_and_flip() -> None:
    plane_a = Plane3D.from_coefficients(0.0, 0.0, 1.0, 0.0)
    plane_b = Plane3D.from_coefficients(0.0, 0.0, -1.0, 0.0).flip()

    assert plane_a == plane_b
    assert plane_a.flip() == plane_b


def test_plane3d_intersection_line() -> None:
    first = Plane3D.from_coefficients(0.0, 0.0, 1.0, 0.0)
    second = Plane3D.from_coefficients(1.0, 0.0, 0.0, 0.0)
    intersection = first.intersect_with_plane(second)

    assert intersection is not None
    point_on_line, direction = intersection
    assert first.is_point_on_plane(point_on_line)
    assert second.is_point_on_plane(point_on_line)
    assert direction == Vector3D(0.0, 1.0, 0.0) or direction == Vector3D(0.0, -1.0, 0.0)


def test_plane3d_invalid_construction() -> None:
    p1 = Point3D(0.0, 0.0, 0.0)
    p2 = Point3D(1.0, 1.0, 1.0)
    p3 = Point3D(2.0, 2.0, 2.0)

    try:
        Plane3D.from_points(p1, p2, p3)
        raise AssertionError("Expected ValueError for collinear points")
    except ValueError:
        pass

    try:
        Plane3D.from_coefficients(0.0, 0.0, 0.0, 1.0)
        raise AssertionError("Expected ValueError for zero normal")
    except ValueError:
        pass
