from fastapi import FastAPI
from fastapi.testclient import TestClient

from application.health import HealthCheckUseCase
from tests.conftest import FakeTelemetryService
from webapi.main import create_app


def _build_test_app(telemetry: FakeTelemetryService | None = None) -> FastAPI:
    app = create_app()
    if telemetry is not None:
        use_case = HealthCheckUseCase(telemetry=telemetry)
        app.state.telemetry = telemetry
        app.state.health_use_case = use_case
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
