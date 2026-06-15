from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider


class TelemetryService:
    def __init__(self, tracer: trace.Tracer, provider: TracerProvider) -> None:
        self._tracer = tracer
        self._provider = provider

    def track_event(self, name: str, attributes: dict | None = None) -> None:
        with self._tracer.start_as_current_span(name) as span:
            if attributes:
                span.set_attributes(attributes)

    def shutdown(self) -> None:
        self._provider.shutdown()
