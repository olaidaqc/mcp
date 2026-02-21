import sys
import unittest
from pathlib import Path

from mcp_manager.startup import startup_run


def test_startup_run_creates_reports(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    def fake_fetch(domain, query, token=None, max_items=10):
        return [{"name": "tool-a", "stargazers_count": 10, "updated_days": 1}]
    env = {
        "AI_HUB_ROOT": str(tmp_path),
        "AI_SCAN_ROOTS": str(tmp_path),
    }
    result = startup_run(env=env, fetcher=fake_fetch)
    assert (tmp_path / "_reports" / "plan.json").exists()
    assert (tmp_path / "_reports" / "recommendations.json").exists()
    assert "plan" in result and "recommendations" in result


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
