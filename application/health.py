class HealthCheckUseCase:
    def __init__(self, telemetry) -> None:
        self._telemetry = telemetry

    def execute(self) -> dict:
        self._telemetry.track_event("health_check_executed")
        return {"status": "healthy"}
