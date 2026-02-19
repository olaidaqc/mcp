import sys
import unittest
from pathlib import Path

from mcp_manager.aihub_structure import ensure_structure


def test_ensure_structure_creates_readmes(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    ensure_structure(tmp_path)
    assert (tmp_path / "Models" / "README.md").exists()
    assert (tmp_path / "_reports").exists()


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
