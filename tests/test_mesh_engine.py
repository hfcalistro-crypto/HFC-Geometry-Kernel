import pytest

from src.mesh import CorruptedMesh, InvalidMeshFile, MeshEngine, MeshData, UnsupportedFormat


def test_mesh_engine_recognizes_supported_mesh_formats():
    engine = MeshEngine()

    assert engine.supports_file("part.obj")
    assert engine.supports_file("scan.STL")
    assert engine.supports_file("cloud.ply")


def test_mesh_engine_rejects_unsupported_formats():
    engine = MeshEngine()

    assert not engine.supports_file("drawing.step")
    assert not engine.supports_file("notes.txt")


def test_mesh_engine_loads_obj_vertices_triangles_bounds_and_statistics(tmp_path):
    mesh_file = tmp_path / "part.obj"
    mesh_file.write_text(
        "\n".join(
            [
                "v 0 0 0",
                "v 1 0 0",
                "v 0 1 0",
                "v 0 0 1",
                "f 1 2 3",
                "f 1 3 4",
            ]
        ),
        encoding="utf-8",
    )

    engine = MeshEngine().load(mesh_file)

    assert engine.is_loaded()
    assert engine.get_vertices() == [
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    ]
    assert engine.get_triangles() == [(0, 1, 2), (0, 2, 3)]
    assert engine.get_bounds() == {"min": (0.0, 0.0, 0.0), "max": (1.0, 1.0, 1.0)}
    assert engine.get_statistics() == {
        "source_path": str(mesh_file),
        "file_format": "obj",
        "vertex_count": 4,
        "triangle_count": 2,
        "edge_count": 5,
        "bounds": {"min": (0.0, 0.0, 0.0), "max": (1.0, 1.0, 1.0)},
    }


def test_mesh_engine_returns_immutable_mesh_data_snapshot(tmp_path):
    mesh_file = tmp_path / "part.obj"
    mesh_file.write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3", encoding="utf-8")

    engine = MeshEngine().load(mesh_file)
    data = engine.get_mesh_data()

    assert isinstance(data, MeshData)
    assert data.vertices == ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0))
    assert data.triangles == ((0, 1, 2),)


def test_mesh_engine_loads_ascii_stl(tmp_path):
    mesh_file = tmp_path / "part.stl"
    mesh_file.write_text(
        "solid part\n"
        "facet normal 0 0 1\n"
        "outer loop\n"
        "vertex 0 0 0\n"
        "vertex 1 0 0\n"
        "vertex 0 1 0\n"
        "endloop\n"
        "endfacet\n"
        "endsolid part\n",
        encoding="utf-8",
    )

    engine = MeshEngine().load(mesh_file)

    assert engine.get_vertices() == [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    assert engine.get_triangles() == [(0, 1, 2)]
    assert engine.get_statistics()["file_format"] == "stl"


def test_mesh_engine_loads_ascii_ply(tmp_path):
    mesh_file = tmp_path / "part.ply"
    mesh_file.write_text(
        "ply\n"
        "format ascii 1.0\n"
        "element vertex 3\n"
        "property float x\n"
        "property float y\n"
        "property float z\n"
        "element face 1\n"
        "property list uchar int vertex_indices\n"
        "end_header\n"
        "0 0 0\n"
        "1 0 0\n"
        "0 1 0\n"
        "3 0 1 2\n",
        encoding="utf-8",
    )

    engine = MeshEngine().load(mesh_file)

    assert engine.get_vertices() == [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    assert engine.get_triangles() == [(0, 1, 2)]
    assert engine.get_statistics()["file_format"] == "ply"


def test_mesh_engine_returns_empty_bounds_before_load():
    engine = MeshEngine()

    assert not engine.is_loaded()
    assert engine.get_bounds() == {"min": None, "max": None}


def test_mesh_engine_clear_resets_loaded_state(tmp_path):
    mesh_file = tmp_path / "part.obj"
    mesh_file.write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3", encoding="utf-8")

    engine = MeshEngine().load(mesh_file)
    engine.clear()

    assert not engine.is_loaded()
    assert engine.get_vertices() == []
    assert engine.get_triangles() == []
    assert engine.get_statistics()["source_path"] is None


def test_mesh_engine_raises_invalid_mesh_file_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.obj"

    with pytest.raises(InvalidMeshFile):
        MeshEngine().load(missing_file)


def test_mesh_engine_raises_unsupported_format(tmp_path):
    mesh_file = tmp_path / "part.step"
    mesh_file.write_text("data", encoding="utf-8")

    with pytest.raises(UnsupportedFormat):
        MeshEngine().load(mesh_file)


def test_mesh_engine_raises_corrupted_mesh_for_invalid_mesh_data(tmp_path):
    mesh_file = tmp_path / "broken.obj"
    mesh_file.write_text("v 0 0 0\nf 1 two 3", encoding="utf-8")

    with pytest.raises(CorruptedMesh):
        MeshEngine().load(mesh_file)


def test_mesh_engine_raises_corrupted_mesh_for_missing_triangle_reference(tmp_path):
    mesh_file = tmp_path / "broken.obj"
    mesh_file.write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 4", encoding="utf-8")

    with pytest.raises(CorruptedMesh):
        MeshEngine().load(mesh_file)


def test_mesh_engine_clears_state_after_failed_load(tmp_path):
    valid_file = tmp_path / "valid.obj"
    broken_file = tmp_path / "broken.obj"
    valid_file.write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3", encoding="utf-8")
    broken_file.write_text("v 0 0 0", encoding="utf-8")

    engine = MeshEngine().load(valid_file)

    with pytest.raises(CorruptedMesh):
        engine.load(broken_file)

    assert not engine.is_loaded()
    assert engine.get_statistics()["source_path"] is None
