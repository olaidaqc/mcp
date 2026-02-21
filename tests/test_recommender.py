import sys
import unittest

from mcp_manager.recommender import score_repo, dedupe_by_capability, pick_best


def test_score_repo_prefers_recent_and_stars():
    repo = {"stargazers_count": 1000, "updated_days": 5}
    score = score_repo(repo)
    assert score > 0


def test_dedupe_by_capability_keeps_best():
    repos = [
        {"name": "A", "capability": "inference", "stargazers_count": 100, "updated_days": 10},
        {"name": "B", "capability": "inference", "stargazers_count": 500, "updated_days": 3},
    ]
    kept = dedupe_by_capability(repos)
    assert len(kept) == 1
    assert kept[0]["name"] == "B"


def test_pick_best_returns_top_repo():
    repos = [
        {"name": "A", "stargazers_count": 100, "updated_days": 10},
        {"name": "B", "stargazers_count": 500, "updated_days": 3},
    ]
    best, alternatives = pick_best(repos)
    assert best["name"] == "B"
    assert len(alternatives) == 1


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
