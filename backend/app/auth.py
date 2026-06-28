"""Simple access-key gate for self-hosted web access."""
from __future__ import annotations

import secrets
from collections.abc import Callable

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.config import settings

AUTH_HEADER = "X-StockOne-Key"
AUTH_QUERY = "access_key"

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginIn(BaseModel):
    key: str = ""


def _configured_key() -> str:
    return settings.app_access_key.strip()


def _matches(candidate: str, expected: str) -> bool:
    return bool(expected) and secrets.compare_digest(candidate, expected)


@router.get("/status")
def status(request: Request) -> dict:
    return {"enabled": bool(_get_key(request))}


@router.post("/login")
def login(req: LoginIn, request: Request):
    key = _get_key(request)
    if not key or _matches(req.key, key):
        return {"ok": True}
    return JSONResponse(status_code=401, content={"detail": "访问 Key 不正确"})


def _get_key(request: Request) -> str:
    getter = getattr(request.app.state, "access_key_getter", _configured_key)
    return getter().strip()


def install_access_key_auth(
    app: FastAPI,
    get_access_key: Callable[[], str] = _configured_key,
) -> None:
    app.state.access_key_getter = get_access_key

    @app.middleware("http")
    async def access_key_auth(request: Request, call_next):
        expected = get_access_key().strip()
        path = request.url.path

        if (
            not expected
            or not path.startswith("/api/")
            or path.startswith("/api/auth/")
        ):
            return await call_next(request)

        candidate = request.headers.get(AUTH_HEADER, "")
        if not candidate:
            candidate = request.query_params.get(AUTH_QUERY, "")

        if _matches(candidate, expected):
            return await call_next(request)

        return JSONResponse(status_code=401, content={"detail": "请先输入访问 Key"})
