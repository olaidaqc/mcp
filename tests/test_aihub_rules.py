import sys
import unittest
from pathlib import Path

from mcp_manager.aihub_rules import load_rules, is_core_file, is_large_file


def test_core_and_large_detection(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    rules = load_rules(tmp_path)
    core = tmp_path / "model.gguf"
    core.write_bytes(b"x")
    assert is_core_file(core, rules)
    big = tmp_path / "big.bin"
    big.write_bytes(b"x" * (rules["large_threshold_bytes"] + 1))
    assert is_large_file(big, rules)


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
