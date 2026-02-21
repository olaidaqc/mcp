import sys
import unittest
from pathlib import Path

from mcp_manager.scan_filters import is_project_dir, should_exclude_path, iter_scan_files


def test_is_project_dir_detects_git(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    (tmp_path / ".git").mkdir()
    assert is_project_dir(tmp_path, markers=["pyproject.toml"]) is True


def test_is_project_dir_detects_marker(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    (tmp_path / "pyproject.toml").write_text("x", encoding="utf-8")
    assert is_project_dir(tmp_path, markers=["pyproject.toml"]) is True


def test_should_exclude_path_blocks_desktop_claude(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    user_home = tmp_path
    path = tmp_path / "Desktop" / "claude" / "file.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
    rules = {"exclude_path_fragments": ["Desktop/claude"], "exclude_dir_names": []}
    assert should_exclude_path(path, rules, user_home) is True


def test_iter_scan_files_skips_project_dirs(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    root = tmp_path / "root"
    project = root / "proj"
    project.mkdir(parents=True)
    (project / ".git").mkdir()
    (project / "llama.txt").write_text("llama", encoding="utf-8")
    keep = root / "keep"
    keep.mkdir(parents=True)
    (keep / "llama.txt").write_text("llama", encoding="utf-8")
    rules = {
        "exclude_dir_names": [".git"],
        "exclude_path_fragments": [],
        "project_markers": ["pyproject.toml"],
    }
    files = list(iter_scan_files([root], rules, user_home=tmp_path))
    paths = [str(p).replace("\\", "/") for p in files]
    assert any("keep/llama.txt" in p for p in paths)
    assert all("proj/llama.txt" not in p for p in paths)


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
