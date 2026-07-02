"""Mesh domain models."""

from dataclasses import dataclass


Vector3 = tuple[float, float, float]
Triangle = tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class MeshBounds:
    """Axis-aligned mesh bounds."""

    minimum: Vector3
    maximum: Vector3

    def as_dict(self) -> dict[str, Vector3]:
        """Return bounds using the public MeshEngine dictionary format."""
        return {"min": self.minimum, "max": self.maximum}


@dataclass(frozen=True, slots=True)
class MeshStatistics:
    """Basic mesh statistics for reverse engineering workflows."""

    source_path: str | None
    file_format: str | None
    vertex_count: int
    triangle_count: int
    edge_count: int
    bounds: dict[str, Vector3 | None]

    def as_dict(self) -> dict[str, object]:
        """Return statistics using a stable dictionary format."""
        return {
            "source_path": self.source_path,
            "file_format": self.file_format,
            "vertex_count": self.vertex_count,
            "triangle_count": self.triangle_count,
            "edge_count": self.edge_count,
            "bounds": self.bounds,
        }


@dataclass(frozen=True, slots=True)
class MeshData:
    """Immutable snapshot of loaded mesh data."""

    vertices: tuple[Vector3, ...]
    triangles: tuple[Triangle, ...]
