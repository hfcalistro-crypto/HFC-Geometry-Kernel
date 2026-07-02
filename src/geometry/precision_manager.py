"""Precision management for the HFC Geometry Kernel.

This module centralizes geometric tolerance handling for the HGK.
It provides a stable and extensible entry point for comparing scalar
values, points, and vectors in a numerically robust way.
"""

from __future__ import annotations

import math
from typing import Sequence, Tuple

Point3 = Tuple[float, float, float]
Vector3 = Tuple[float, float, float]


class PrecisionManager:
    """Centralize geometric tolerance policies for HGK.

    The manager defines default tolerances for linear and angular
    comparisons and exposes safe comparison helpers for scalar values,
    points, and vectors. The implementation is intentionally simple,
    dependency-free, and prepared for future extension.
    """

    def __init__(
        self,
        linear_tolerance: float = 1e-6,
        angular_tolerance: float = 1e-6,
    ) -> None:
        """Initialize the precision manager with default tolerances.

        Args:
            linear_tolerance: Maximum allowed linear deviation in millimeters.
            angular_tolerance: Maximum allowed angular deviation in radians.
        """
        self._linear_tolerance = self._validate_tolerance(
            linear_tolerance,
            "linear_tolerance",
        )
        self._angular_tolerance = self._validate_tolerance(
            angular_tolerance,
            "angular_tolerance",
        )

    def get_linear_tolerance(self) -> float:
        """Return the configured linear tolerance in millimeters."""
        return self._linear_tolerance

    def get_angular_tolerance(self) -> float:
        """Return the configured angular tolerance in radians."""
        return self._angular_tolerance

    def set_linear_tolerance(self, tolerance: float) -> None:
        """Set a new linear tolerance in millimeters.

        Args:
            tolerance: Positive tolerance value.
        """
        self._linear_tolerance = self._validate_tolerance(tolerance, "tolerance")

    def set_angular_tolerance(self, tolerance: float) -> None:
        """Set a new angular tolerance in radians.

        Args:
            tolerance: Positive tolerance value.
        """
        self._angular_tolerance = self._validate_tolerance(tolerance, "tolerance")

    def compare_floats(
        self,
        left: float,
        right: float,
        *,
        tolerance: float | None = None,
    ) -> bool:
        """Compare two floating-point values using a safe tolerance.

        The comparison is based on absolute and relative deviation,
        which makes it robust for values near zero and for larger values.

        Args:
            left: First value to compare.
            right: Second value to compare.
            tolerance: Optional override for the comparison tolerance.

        Returns:
            True when the values are considered equal within tolerance.
        """
        active_tolerance = self._resolve_tolerance(tolerance)
        return abs(left - right) <= max(
            active_tolerance,
            active_tolerance * max(abs(left), abs(right)),
        )

    def compare_points(
        self,
        left: Point3,
        right: Point3,
        *,
        tolerance: float | None = None,
    ) -> bool:
        """Compare two 3D points using the configured linear tolerance.

        Args:
            left: First point as a tuple of three coordinates.
            right: Second point as a tuple of three coordinates.
            tolerance: Optional override for the comparison tolerance.

        Returns:
            True when all coordinate components are within tolerance.
        """
        self._validate_point(left, "left")
        self._validate_point(right, "right")
        active_tolerance = self._resolve_tolerance(tolerance)
        return all(
            self.compare_floats(component_left, component_right, tolerance=active_tolerance)
            for component_left, component_right in zip(left, right)
        )

    def compare_vectors(
        self,
        left: Vector3,
        right: Vector3,
        *,
        tolerance: float | None = None,
    ) -> bool:
        """Compare two 3D vectors using the configured linear tolerance.

        Args:
            left: First vector as a tuple of three components.
            right: Second vector as a tuple of three components.
            tolerance: Optional override for the comparison tolerance.

        Returns:
            True when all vector components are within tolerance.
        """
        self._validate_vector(left, "left")
        self._validate_vector(right, "right")
        active_tolerance = self._resolve_tolerance(tolerance)
        return all(
            self.compare_floats(component_left, component_right, tolerance=active_tolerance)
            for component_left, component_right in zip(left, right)
        )

    def _validate_tolerance(self, tolerance: float, name: str) -> float:
        """Validate that a tolerance value is positive and finite."""
        if not isinstance(tolerance, (int, float)):
            raise TypeError(f"{name} must be a real number")
        numeric_tolerance = float(tolerance)
        if not math.isfinite(numeric_tolerance) or numeric_tolerance <= 0.0:
            raise ValueError(f"{name} must be a positive finite number")
        return numeric_tolerance

    def _resolve_tolerance(self, tolerance: float | None) -> float:
        """Return the effective tolerance for a comparison operation."""
        if tolerance is None:
            return self._linear_tolerance
        return self._validate_tolerance(tolerance, "tolerance")

    def _validate_point(self, point: Sequence[float], name: str) -> None:
        """Ensure that a point-like sequence contains three numeric values."""
        if len(point) != 3:
            raise ValueError(f"{name} must contain exactly three coordinates")
        for index, value in enumerate(point):
            if not isinstance(value, (int, float)):
                raise TypeError(f"{name}[{index}] must be a real number")

    def _validate_vector(self, vector: Sequence[float], name: str) -> None:
        """Ensure that a vector-like sequence contains three numeric values."""
        if len(vector) != 3:
            raise ValueError(f"{name} must contain exactly three components")
        for index, value in enumerate(vector):
            if not isinstance(value, (int, float)):
                raise TypeError(f"{name}[{index}] must be a real number")


__all__ = ["PrecisionManager", "Point3", "Vector3"]
