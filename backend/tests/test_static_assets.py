from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.static_assets import install_static_routes


def test_favicon_is_served_as_svg_before_spa_fallback(tmp_path):
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    (static_dir / "assets").mkdir()
    (static_dir / "favicon.svg").write_text("<svg></svg>", encoding="utf-8")
    (static_dir / "index.html").write_text("<!doctype html><title>App</title>", encoding="utf-8")

    app = FastAPI()
    install_static_routes(app, static_dir)

    res = TestClient(app).get("/favicon.svg")

    assert res.status_code == 200
    assert res.headers["content-type"].startswith("image/svg+xml")
    assert res.text == "<svg></svg>"
