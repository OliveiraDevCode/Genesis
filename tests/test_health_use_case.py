from application.use_cases.health import HealthCheckUseCase
from tests.conftest import FakeTelemetryService


def test_health_check_returns_healthy():
    telemetry = FakeTelemetryService()
    use_case = HealthCheckUseCase(telemetry=telemetry)

    result = use_case.execute()

    assert result == {"status": "healthy"}


def test_health_check_tracks_event():
    telemetry = FakeTelemetryService()
    use_case = HealthCheckUseCase(telemetry=telemetry)

    use_case.execute()

    assert len(telemetry.events) == 1
    assert telemetry.events[0]["name"] == "health_check_executed"


def test_health_use_case_accepts_fake_telemetry():
    telemetry = FakeTelemetryService()
    use_case = HealthCheckUseCase(telemetry=telemetry)

    use_case.execute()

    assert isinstance(use_case._telemetry, FakeTelemetryService)
