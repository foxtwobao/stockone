from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.auth import AUTH_HEADER, install_access_key_auth, router


def _client(access_key: str) -> TestClient:
    app = FastAPI()
    install_access_key_auth(app, get_access_key=lambda: access_key)
    app.include_router(router)

    @app.get("/api/private")
    def private() -> dict:
        return {"ok": True}

    return TestClient(app)


def test_auth_disabled_when_env_key_is_empty():
    client = _client("")

    assert client.get("/api/private").status_code == 200
    assert client.get("/api/auth/status").json() == {"enabled": False}


def test_login_accepts_configured_key_and_rejects_wrong_key():
    client = _client("secret")

    assert client.post("/api/auth/login", json={"key": "wrong"}).status_code == 401
    assert client.post("/api/auth/login", json={"key": "secret"}).json() == {"ok": True}


def test_api_requires_key_when_configured():
    client = _client("secret")

    assert client.get("/api/private").status_code == 401
    assert client.get("/api/private", headers={AUTH_HEADER: "secret"}).status_code == 200


def test_eventsource_can_authorize_with_query_param():
    client = _client("secret")

    assert client.get("/api/private?access_key=secret").status_code == 200
