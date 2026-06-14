from application.interfaces.telemetry import TelemetryPort


class HealthCheckUseCase:

    def __init__(self, telemetry: TelemetryPort) -> None:
        self._telemetry = telemetry

    def execute(self) -> dict:
        self._telemetry.track_event("health_check_executed")
        return {"status": "healthy"}
