from fastapi import FastAPI
from fastapi.testclient import TestClient

from application.use_cases.health import HealthCheckUseCase
from tests.conftest import FakeTelemetryService
from webapi.container import Container
from webapi.routes import routers
from webapi.settings import Settings


def _build_test_app(telemetry: FakeTelemetryService | None = None) -> FastAPI:
    """Build a minimal FastAPI app for integration testing.

    Uses a pre-wired Container but lets callers inject a FakeTelemetryService
    so that tests can assert on telemetry events.
    """
    container = Container.create()

    if telemetry is not None:
        container = Container(
            settings=container.settings,
            telemetry_service=telemetry,
            health_use_case=HealthCheckUseCase(telemetry=telemetry),
        )

    app = FastAPI(title=container.settings.service_name)
    app.state.telemetry_service = container.telemetry_service
    app.state.settings = container.settings
    app.state.health_use_case = container.health_use_case

    for router in routers:
        app.include_router(router)

    return app


def test_health_endpoint_returns_200():
    app = _build_test_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"


def test_health_endpoint_includes_service_name():
    app = _build_test_app()
    client = TestClient(app)

    response = client.get("/health")
    data = response.json()

    assert "service" in data
    assert "environment" in data


def test_health_endpoint_uses_telemetry():
    telemetry = FakeTelemetryService()
    app = _build_test_app(telemetry=telemetry)
    client = TestClient(app)

    client.get("/health")

    assert any(
        e["name"] == "health_check_executed" for e in telemetry.events
    )


def test_health_route_is_registered():
    """Verify /health appears in the URL table."""
    app = _build_test_app()
    paths = _collect_route_paths(app.router)
    assert "/health" in paths


def _collect_route_paths(router) -> set:
    """Recursively collect path strings from a router and its sub-routers."""
    paths = set()
    for route in router.routes:
        if hasattr(route, "path"):
            paths.add(route.path)
        # _IncludedRouter wraps the original APIRouter in .original_router
        if hasattr(route, "original_router"):
            paths.update(_collect_route_paths(route.original_router))
    return paths
