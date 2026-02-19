import sys
import unittest

from mcp_manager import paths


def test_paths_resolve_repo_and_user_dirs():
    p = paths.ProjectPaths()
    assert p.repo_root is not None
    assert p.user_home is not None


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
