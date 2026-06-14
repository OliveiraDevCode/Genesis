from fastapi import Request

from application.use_cases.health import HealthCheckUseCase
from infrastructure.observability.telemetry_service import TelemetryService
from webapi.settings import Settings


def get_telemetry_service(request: Request) -> TelemetryService:
    return request.app.state.telemetry_service


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_health_use_case(request: Request) -> HealthCheckUseCase:
    return request.app.state.health_use_case
