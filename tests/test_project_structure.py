from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_main_project_directories_exist():
    expected_directories = [
        "docs",
        "src",
        "src/core",
        "src/geometry",
        "src/mesh",
        "src/reverse",
        "src/ai",
        "src/viewer",
        "src/export",
        "src/ui",
        "src/plugins",
        "tests",
        "samples",
        "output",
        "assets",
    ]

    missing = [
        directory
        for directory in expected_directories
        if not (PROJECT_ROOT / directory).is_dir()
    ]

    assert not missing, f"Missing project directories: {missing}"
