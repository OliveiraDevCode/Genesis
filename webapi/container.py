from contextlib import asynccontextmanager
from dataclasses import dataclass

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
    """Application composition root.

    Wires all dependencies explicitly. Created once at startup and frozen.
    This is the only place where infrastructure and application objects
    are constructed and wired together.
    """

    settings: Settings
    telemetry_service: TelemetryService
    health_use_case: HealthCheckUseCase

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def create(cls) -> "Container":
        """Build the fully-wired application from scratch.

        Call order:
          1. Settings  (configuration)
          2. Tracer    (observability infrastructure)
          3. Services  (application services that depend on infrastructure)
          4. Use cases (application use cases that depend on services)
        """
        settings = Settings.load()

        tracer = cls._create_tracer(settings)

        telemetry_service = TelemetryService(tracer=tracer)
        health_use_case = HealthCheckUseCase(telemetry=telemetry_service)

        return cls(
            settings=settings,
            telemetry_service=telemetry_service,
            health_use_case=health_use_case,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """FastAPI lifespan handler — manages startup and shutdown."""
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

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _create_tracer(settings: Settings) -> trace.Tracer:
        """Create and configure the OpenTelemetry tracer provider.

        The provider is registered globally ONCE here so that
        FastAPI instrumentation can find it. No other code should
        call trace.set_tracer_provider().
        """
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

        trace.set_tracer_provider(provider)
        return trace.get_tracer(settings.service_name)
