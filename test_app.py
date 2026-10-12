
from app import app


def test_health():
    assert app.test_client().get("/health").data == b"OK"


def test_home():
    resp = app.test_client().get("/")
    assert resp.status_code == 200
    assert b"CT Group" in resp.data


def test_kpi():
    resp = app.test_client().get("/kpi")
    assert resp.status_code == 200
    assert resp.get_json()[0]["target"] == "95%"