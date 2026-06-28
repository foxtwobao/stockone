from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import auth as auth_api
from app.services import auth


def _client(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.setattr(auth, "_path", lambda: tmp_path / "auth.json")
    auth._sessions.clear()
    auth_api._fail_counter.clear()
    app = FastAPI()
    app.include_router(auth_api.router)
    return TestClient(app)


def test_setup_requires_local_network(tmp_path, monkeypatch):
    client = _client(tmp_path, monkeypatch)

    res = client.post(
        "/api/auth/setup",
        json={"password": "secret1"},
        headers={"x-forwarded-for": "8.8.8.8"},
    )

    assert res.status_code == 403


def test_setup_login_status_and_logout(tmp_path, monkeypatch):
    client = _client(tmp_path, monkeypatch)

    setup = client.post(
        "/api/auth/setup",
        json={"password": "secret1"},
        headers={"x-forwarded-for": "127.0.0.1"},
    )
    assert setup.status_code == 200

    login = client.post("/api/auth/login", json={"password": "secret1"})
    assert login.status_code == 200
    assert auth_api.COOKIE_NAME in login.cookies

    status = client.get("/api/auth/status")
    assert status.json() == {"configured": True, "authenticated": True}

    logout = client.post("/api/auth/logout")
    assert logout.status_code == 200

    status = client.get("/api/auth/status")
    assert status.json() == {"configured": True, "authenticated": False}
