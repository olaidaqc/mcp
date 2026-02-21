import sys
import unittest
import json
from pathlib import Path

from mcp_manager.recommendations import refresh_recommendations, load_recommendations


def test_refresh_recommendations_writes_report(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    def fake_fetch(domain, query, token=None, max_items=10):
        return [
            {"name": "tool-a", "stargazers_count": 100, "updated_days": 5, "description": "llm tool", "topics": []},
            {"name": "tool-b", "stargazers_count": 50, "updated_days": 1, "description": "llm tool", "topics": []},
        ]
    report = refresh_recommendations(hub_root=tmp_path, fetcher=fake_fetch)
    report_path = tmp_path / "_reports" / "recommendations.json"
    assert report_path.exists()
    loaded = json.loads(report_path.read_text(encoding="utf-8"))
    assert "domains" in loaded
    assert loaded["domains"][0]["best"]["name"] == "tool-a"


def test_load_recommendations_empty_when_missing(tmp_path=None):
    import tempfile
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())
    assert load_recommendations(tmp_path) == {"domains": [], "updated_at": None}


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
