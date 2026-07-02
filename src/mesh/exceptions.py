"""Mesh domain exceptions."""


class InvalidMeshFile(Exception):
    """Raised when a mesh file cannot be used by the mesh engine."""


class UnsupportedFormat(InvalidMeshFile):
    """Raised when a mesh file extension is not supported."""


class CorruptedMesh(InvalidMeshFile):
    """Raised when mesh data cannot be parsed into a valid mesh."""
