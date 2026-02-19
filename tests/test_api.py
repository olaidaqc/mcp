import sys
import unittest
import os
import tempfile
from pathlib import Path

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


def test_scan_endpoint():
    root = Path(tempfile.mkdtemp())
    sample = root / "demo.gguf"
    sample.write_bytes(b"x")
    os.environ["AI_HUB_ROOT"] = str(root)
    os.environ["AI_SCAN_ROOTS"] = str(root)
    client = TestClient(app)
    resp = client.post("/api/scan")
    assert resp.status_code == 200


def test_apply_auto_endpoint():
    client = TestClient(app)
    resp = client.post("/api/apply-auto")
    assert resp.status_code == 200


def test_confirm_endpoint():
    client = TestClient(app)
    resp = client.post("/api/confirm", json={"paths": []})
    assert resp.status_code == 200


def load_tests(loader, tests, pattern):
    module = sys.modules[__name__]
    for name, obj in vars(module).items():
        if name.startswith("test_") and callable(obj):
            tests.addTest(unittest.FunctionTestCase(obj))
    return tests
