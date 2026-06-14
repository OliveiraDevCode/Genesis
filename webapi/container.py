from contextlib import asynccontextmanager
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from application.constants.events import TelemetryEvents
from application.use_cases.health import HealthCheckUseCase
from infrastructure.observability.telemetry_service import TelemetryService
from webapi.settings import Settings


@dataclass(frozen=True)
class Container:
    settings: Settings
    telemetry_service: TelemetryService
    health_use_case: HealthCheckUseCase

    @classmethod
    def create(cls) -> "Container":
        settings = Settings.load()
        tracer = cls._create_tracer(settings)
        telemetry_service = TelemetryService(tracer=tracer)
        health_use_case = HealthCheckUseCase(telemetry=telemetry_service)

        return cls(
            settings=settings,
            telemetry_service=telemetry_service,
            health_use_case=health_use_case,
        )

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        self._startup()
        yield
        self._shutdown()

    def _startup(self) -> None:
        self.telemetry_service.track_event(TelemetryEvents.APPLICATION_STARTED)

    def _shutdown(self) -> None:
        try:
            self.telemetry_service.track_event(TelemetryEvents.APPLICATION_STOPPED)
        finally:
            self.telemetry_service.shutdown()

    @staticmethod
    def _create_tracer(settings: Settings) -> trace.Tracer:
        resource = Resource.create(
            {
                "service.name": settings.service_name,
                "deployment.environment": settings.environment,
            }
        )

        provider = TracerProvider(resource=resource)

        if settings.otel_exporter == "console":
            provider.add_span_processor(
                SimpleSpanProcessor(ConsoleSpanExporter())
            )

        _set_global_provider_once(provider)
        return trace.get_tracer(settings.service_name)


_tracer_provider_set = False


def _set_global_provider_once(provider: TracerProvider) -> None:
    global _tracer_provider_set
    if not _tracer_provider_set:
        trace.set_tracer_provider(provider)
        _tracer_provider_set = True
    else:
        logger.debug("TracerProvider already set globally — skipping")
