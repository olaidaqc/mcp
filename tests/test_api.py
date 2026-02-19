import sys
import unittest

from fastapi.testclient import TestClient
from web.server import app


def test_status_endpoint():
    client = TestClient(app)
    resp = client.get("/api/status")
    assert resp.status_code == 200


def test_static_index_loads():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200


def test_tools_endpoint():
    client = TestClient(app)
    resp = client.get("/api/tools")
    assert resp.status_code == 200


def test_plan_endpoint():
    client = TestClient(app)
    resp = client.get("/api/plan")
    assert resp.status_code == 200


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
