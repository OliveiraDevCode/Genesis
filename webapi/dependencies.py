from fastapi import Request

from application.use_cases.health import HealthCheckUseCase
from infrastructure.observability.telemetry_service import TelemetryService
from webapi.settings import Settings

"""FastAPI dependency-injection functions.

Each function extracts a pre-wired dependency from app.state.
These are the only places where app.state is accessed for DI.
Routes declare their dependencies explicitly via Depends().
"""


def get_telemetry_service(request: Request) -> TelemetryService:
    return request.app.state.telemetry_service


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_health_use_case(request: Request) -> HealthCheckUseCase:
    return request.app.state.health_use_case
