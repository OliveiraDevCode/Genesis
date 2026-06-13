from fastapi import FastAPI
from contextlib import asynccontextmanager

from webapi.startup.telemetry import configure_telemetry
from infrastructure.observability.constants.events import TelemetryEvents


@asynccontextmanager
async def lifespan(app: FastAPI):
    telemetry = configure_telemetry()

    app.state.telemetry = telemetry
    app.state.started = False

    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        FastAPIInstrumentor.instrument_app(app)
    except ImportError:
        pass

    telemetry.track_event(
        TelemetryEvents.APPLICATION_STARTED
    )

    app.state.started = True

    yield

    app.state.started = False

    try:
        telemetry.track_event(
            TelemetryEvents.APPLICATION_STOPPED
        )
    finally:
        telemetry.shutdown()