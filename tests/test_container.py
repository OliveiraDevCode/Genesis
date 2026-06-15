from application.health import HealthCheckUseCase
from infrastructure.telemetry import TelemetryService
from webapi.main import create_app


def test_create_app_succeeds():
    app = create_app()
    assert app.title is not None


def test_create_app_wires_telemetry():
    app = create_app()
    assert isinstance(app.state.telemetry, TelemetryService)


def test_create_app_wires_health_use_case():
    app = create_app()
    assert isinstance(app.state.health_use_case, HealthCheckUseCase)


def test_create_app_shares_telemetry_instance():
    app = create_app()
    assert app.state.health_use_case._telemetry is app.state.telemetry
