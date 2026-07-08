import pytest

from src.geometry.boundingbox3d import BoundingBox3D
from src.geometry.point3d import Point3D


def test_bounding_box_empty_creation() -> None:
    box = BoundingBox3D.empty()

    assert box.is_empty()
    assert box.contains(Point3D(0.0, 0.0, 0.0)) is False


def test_bounding_box_from_points_and_expand() -> None:
    box = BoundingBox3D.from_points(
        [
            Point3D(1.0, 2.0, 3.0),
            Point3D(4.0, 5.0, 6.0),
        ]
    )

    assert box.contains(Point3D(2.0, 3.0, 4.0)) is True
    assert box.contains(Point3D(10.0, 10.0, 10.0)) is False
    assert box.center() == Point3D(2.5, 3.5, 4.5)
    assert box.size() == (3.0, 3.0, 3.0)
    assert box.width() == 3.0
    assert box.height() == 3.0
    assert box.depth() == 3.0
    assert box.volume() == 27.0

    expanded = box.expand(Point3D(-1.0, -1.0, -1.0))
    assert expanded.contains(Point3D(-1.0, -1.0, -1.0)) is True
    assert expanded.size() == (5.0, 6.0, 7.0)


def test_bounding_box_union_and_intersects() -> None:
    left = BoundingBox3D.from_points([Point3D(0.0, 0.0, 0.0), Point3D(2.0, 2.0, 2.0)])
    right = BoundingBox3D.from_points([Point3D(1.0, 1.0, 1.0), Point3D(3.0, 3.0, 3.0)])

    union_box = left.union(right)
    assert union_box.size() == (3.0, 3.0, 3.0)
    assert union_box.contains(Point3D(0.0, 0.0, 0.0)) is True
    assert union_box.contains(Point3D(3.0, 3.0, 3.0)) is True

    assert left.intersects(right) is True
    assert left.intersects(BoundingBox3D.from_points([Point3D(10.0, 10.0, 10.0)])) is False


def test_bounding_box_invalid_inputs() -> None:
    with pytest.raises(TypeError):
        BoundingBox3D.from_points([Point3D(0.0, 0.0, 0.0), "invalid"])

    with pytest.raises(TypeError):
        BoundingBox3D.empty().expand("invalid")

    with pytest.raises(TypeError):
        BoundingBox3D.empty().contains("invalid")

    with pytest.raises(TypeError):
        BoundingBox3D.empty().union("invalid")

    with pytest.raises(TypeError):
        BoundingBox3D.empty().intersects("invalid")
