import pytest

from src.geometry.precision_manager import PrecisionManager


def test_compare_floats_accepts_values_within_tolerance() -> None:
    manager = PrecisionManager(linear_tolerance=1e-6)

    assert manager.compare_floats(1.0, 1.0 + 5e-7)
    assert not manager.compare_floats(1.0, 1.0 + 2e-6)


def test_compare_points_uses_linear_tolerance() -> None:
    manager = PrecisionManager(linear_tolerance=1e-6)

    assert manager.compare_points((0.0, 0.0, 0.0), (1e-7, 0.0, 0.0))
    assert not manager.compare_points((0.0, 0.0, 0.0), (2e-6, 0.0, 0.0))


def test_compare_vectors_uses_linear_tolerance() -> None:
    manager = PrecisionManager(linear_tolerance=1e-6)

    assert manager.compare_vectors((1.0, 0.0, 0.0), (1.0 + 5e-7, 0.0, 0.0))
    assert not manager.compare_vectors((1.0, 0.0, 0.0), (1.0 + 2e-6, 0.0, 0.0))


def test_tolerance_validation_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        PrecisionManager(linear_tolerance=0.0)

    with pytest.raises(ValueError):
        PrecisionManager(angular_tolerance=-1.0)

    with pytest.raises(TypeError):
        PrecisionManager(linear_tolerance="invalid")


def test_custom_tolerance_override_is_supported() -> None:
    manager = PrecisionManager(linear_tolerance=1e-6)

    assert manager.compare_floats(1.0, 1.0 + 5e-7, tolerance=1e-5)
    assert not manager.compare_floats(1.0, 1.0 + 2e-5, tolerance=1e-6)
