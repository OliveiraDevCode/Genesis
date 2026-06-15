from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from application.health import HealthCheckUseCase
from infrastructure.telemetry import TelemetryService

SERVICE_NAME = "genesis"
ENVIRONMENT = "development"
OTEL_EXPORTER = "console"


def get_health_use_case(request: Request) -> HealthCheckUseCase:
    return request.app.state.health_use_case


def create_app() -> FastAPI:
    resource = Resource.create(
        {
            "service.name": SERVICE_NAME,
            "deployment.environment": ENVIRONMENT,
        }
    )
    provider = TracerProvider(resource=resource)
    if OTEL_EXPORTER == "console":
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(SERVICE_NAME)

    telemetry_service = TelemetryService(tracer=tracer, provider=provider)
    health_use_case = HealthCheckUseCase(telemetry=telemetry_service)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        telemetry_service.track_event("application_started")
        yield
        telemetry_service.shutdown()

    app = FastAPI(title=SERVICE_NAME, lifespan=lifespan)
    app.state.telemetry = telemetry_service
    app.state.health_use_case = health_use_case

    @app.get("/health")
    async def health(
        use_case: HealthCheckUseCase = Depends(get_health_use_case),
    ):
        result = use_case.execute()
        result["service"] = SERVICE_NAME
        result["environment"] = ENVIRONMENT
        return result

    return app


app = create_app()
