from infrastructure.observability.services.telemetry import TelemetryService


class FakeSpan:
    def __init__(self):
        self.attributes = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def set_attributes(self, attributes):
        self.attributes.update(attributes)


class FakeTracer:
    def __init__(self):
        self.started_span_name = None
        self.span = FakeSpan()

    def start_as_current_span(self, event_name):
        self.started_span_name = event_name
        return self.span


def test_track_event_starts_span_and_adds_attributes():
    tracer = FakeTracer()
    telemetry = TelemetryService(tracer)

    telemetry.track_event("application_started", {"component": "webapi"})

    assert tracer.started_span_name == "application_started"
    assert tracer.span.attributes == {"component": "webapi"}
