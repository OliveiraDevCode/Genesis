import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TelemetrySettings:
    service_name: str
    enabled: bool = True
    exporter: str = "console"
    environment: str = "development"

    @classmethod
    def from_environment(cls, default_service_name: str):
        return cls(
            service_name=os.getenv("GENESIS_SERVICE_NAME", default_service_name),
            enabled=os.getenv("GENESIS_TELEMETRY_ENABLED", "true").lower() == "true",
            exporter=os.getenv("GENESIS_OTEL_EXPORTER", "console").lower(),
            environment=os.getenv("GENESIS_ENVIRONMENT", "development"),
        )
