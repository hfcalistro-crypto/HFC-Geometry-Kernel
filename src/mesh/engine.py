"""Proprietary mesh engine implementation."""

from dataclasses import dataclass, field
from pathlib import Path

from .exceptions import CorruptedMesh, InvalidMeshFile, UnsupportedFormat
from .models import MeshBounds, MeshData, MeshStatistics, Triangle, Vector3


@dataclass(slots=True)
class MeshEngine:
    """Coordinates mesh loading, validation, and inspection operations."""

    supported_extensions: tuple[str, ...] = field(
        default_factory=lambda: (".obj", ".stl", ".ply")
    )
    _vertices: list[Vector3] = field(default_factory=list, init=False)
    _triangles: list[Triangle] = field(default_factory=list, init=False)
    _source_path: Path | None = field(default=None, init=False)
    _file_format: str | None = field(default=None, init=False)

    def supports_file(self, file_path: str | Path) -> bool:
        """Return whether the mesh file extension is recognized."""
        suffix = Path(file_path).suffix.lower()
        return suffix in self.supported_extensions

    def load(self, file_path: str | Path) -> "MeshEngine":
        """Load a mesh file and store its vertices and triangles."""
        path = Path(file_path)

        if not path.is_file():
            raise InvalidMeshFile(f"Mesh file not found: {path}")

        if not self.supports_file(path):
            raise UnsupportedFormat(f"Unsupported mesh format: {path.suffix}")

        self.clear()
        self._source_path = path
        self._file_format = path.suffix.lower().lstrip(".")

        try:
            if path.suffix.lower() == ".obj":
                self._load_obj(path)
            elif path.suffix.lower() == ".stl":
                self._load_ascii_stl(path)
            elif path.suffix.lower() == ".ply":
                self._load_ascii_ply(path)

            self._validate_loaded_mesh(path)
        except CorruptedMesh:
            self.clear()
            raise
        except (IndexError, OSError, UnicodeDecodeError, ValueError) as error:
            self.clear()
            raise CorruptedMesh(f"Corrupted mesh file: {path}") from error

        return self

    def clear(self) -> None:
        """Clear the currently loaded mesh state."""
        self._vertices.clear()
        self._triangles.clear()
        self._source_path = None
        self._file_format = None

    def is_loaded(self) -> bool:
        """Return whether a valid mesh is currently loaded."""
        return bool(self._vertices and self._triangles)

    def get_vertices(self) -> list[Vector3]:
        """Return a copy of the loaded mesh vertices."""
        return list(self._vertices)

    def get_triangles(self) -> list[Triangle]:
        """Return a copy of the loaded mesh triangles."""
        return list(self._triangles)

    def get_mesh_data(self) -> MeshData:
        """Return an immutable snapshot of the loaded mesh data."""
        return MeshData(vertices=tuple(self._vertices), triangles=tuple(self._triangles))

    def get_bounds(self) -> dict[str, Vector3 | None]:
        """Return axis-aligned bounds for the loaded mesh."""
        bounds = self._calculate_bounds()
        if bounds is None:
            return {"min": None, "max": None}
        return bounds.as_dict()

    def get_statistics(self) -> dict[str, object]:
        """Return basic mesh statistics."""
        return MeshStatistics(
            source_path=str(self._source_path) if self._source_path else None,
            file_format=self._file_format,
            vertex_count=len(self._vertices),
            triangle_count=len(self._triangles),
            edge_count=self._count_unique_edges(),
            bounds=self.get_bounds(),
        ).as_dict()

    def _load_obj(self, path: Path) -> None:
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if parts[0] == "v" and len(parts) >= 4:
                self._vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif parts[0] == "f" and len(parts) >= 4:
                indices = [self._parse_obj_index(token) for token in parts[1:]]
                self._add_face(indices)

    def _load_ascii_stl(self, path: Path) -> None:
        current_vertices: list[int] = []

        for raw_line in path.read_text(encoding="utf-8").splitlines():
            parts = raw_line.strip().split()
            if len(parts) == 4 and parts[0].lower() == "vertex":
                vertex = (float(parts[1]), float(parts[2]), float(parts[3]))
                self._vertices.append(vertex)
                current_vertices.append(len(self._vertices) - 1)

                if len(current_vertices) == 3:
                    self._triangles.append(
                        (current_vertices[0], current_vertices[1], current_vertices[2])
                    )
                    current_vertices = []

    def _load_ascii_ply(self, path: Path) -> None:
        lines = path.read_text(encoding="utf-8").splitlines()
        vertex_count = 0
        face_count = 0
        header_end = None

        for index, raw_line in enumerate(lines):
            line = raw_line.strip()
            if line.startswith("element vertex"):
                vertex_count = int(line.split()[2])
            elif line.startswith("element face"):
                face_count = int(line.split()[2])
            elif line == "end_header":
                header_end = index + 1
                break

        if header_end is None:
            raise CorruptedMesh("Invalid PLY file: missing end_header")

        vertex_lines = lines[header_end : header_end + vertex_count]
        face_lines = lines[header_end + vertex_count : header_end + vertex_count + face_count]

        if len(vertex_lines) != vertex_count or len(face_lines) != face_count:
            raise CorruptedMesh("Invalid PLY file: declared counts do not match data")

        for raw_line in vertex_lines:
            parts = raw_line.split()
            self._vertices.append((float(parts[0]), float(parts[1]), float(parts[2])))

        for raw_line in face_lines:
            parts = raw_line.split()
            count = int(parts[0])
            indices = [int(value) for value in parts[1 : count + 1]]
            self._add_face(indices)

    def _parse_obj_index(self, token: str) -> int:
        raw_index = int(token.split("/")[0])
        if raw_index == 0:
            raise CorruptedMesh("OBJ indices are 1-based and cannot be zero")
        if raw_index < 0:
            return len(self._vertices) + raw_index
        return raw_index - 1

    def _add_face(self, indices: list[int]) -> None:
        if len(indices) < 3:
            raise CorruptedMesh("A mesh face must have at least three vertices")

        for offset in range(1, len(indices) - 1):
            self._triangles.append((indices[0], indices[offset], indices[offset + 1]))

    def _validate_loaded_mesh(self, path: Path) -> None:
        if not self._vertices:
            raise CorruptedMesh(f"Mesh has no vertices: {path}")
        if not self._triangles:
            raise CorruptedMesh(f"Mesh has no triangles: {path}")

        vertex_count = len(self._vertices)
        for triangle in self._triangles:
            if any(index < 0 or index >= vertex_count for index in triangle):
                raise CorruptedMesh(f"Mesh triangle references missing vertices: {path}")
            if len(set(triangle)) != 3:
                raise CorruptedMesh(f"Mesh contains a degenerate triangle: {path}")

    def _calculate_bounds(self) -> MeshBounds | None:
        if not self._vertices:
            return None

        xs, ys, zs = zip(*self._vertices)
        return MeshBounds(
            minimum=(min(xs), min(ys), min(zs)),
            maximum=(max(xs), max(ys), max(zs)),
        )

    def _count_unique_edges(self) -> int:
        edges: set[tuple[int, int]] = set()
        for a, b, c in self._triangles:
            edges.add(tuple(sorted((a, b))))
            edges.add(tuple(sorted((b, c))))
            edges.add(tuple(sorted((c, a))))
        return len(edges)
