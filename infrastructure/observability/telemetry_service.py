from opentelemetry import trace

from application.interfaces.telemetry import TelemetryPort


class TelemetryService(TelemetryPort):

    def __init__(self, tracer: trace.Tracer) -> None:
        self._tracer = tracer

    def track_event(self, name: str, attributes: dict | None = None) -> None:
        with self._tracer.start_as_current_span(name) as span:
            if attributes:
                span.set_attributes(attributes)

    def track_exception(
        self, exception: Exception, attributes: dict | None = None
    ) -> None:
        with self._tracer.start_as_current_span("exception") as span:
            span.record_exception(exception)
            if attributes:
                span.set_attributes(attributes)

    def shutdown(self) -> None:
        provider = trace.get_tracer_provider()
        if hasattr(provider, "shutdown"):
            provider.shutdown()
