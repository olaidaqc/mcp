import sys
import unittest

from mcp_manager.config import load_json_config


def test_load_config_supports_utf8_bom(tmp_path=None):
    import tempfile
    from pathlib import Path

    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    p = tmp_path / "cfg.json"
    p.write_text("\ufeff{\"name\":\"test\"}", encoding="utf-8")
    data = load_json_config(p)
    assert data["name"] == "test"


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
