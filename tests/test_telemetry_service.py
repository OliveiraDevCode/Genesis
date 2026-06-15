from unittest.mock import MagicMock

from infrastructure.telemetry import TelemetryService


def test_track_event_starts_span_and_adds_attributes():
    tracer = MagicMock()
    provider = MagicMock()
    span = MagicMock()
    tracer.start_as_current_span.return_value.__enter__.return_value = span

    telemetry = TelemetryService(tracer=tracer, provider=provider)
    telemetry.track_event("application_started", {"component": "webapi"})

    tracer.start_as_current_span.assert_called_once_with("application_started")
    span.set_attributes.assert_called_once_with({"component": "webapi"})


def test_track_event_without_attributes():
    tracer = MagicMock()
    provider = MagicMock()
    span = MagicMock()
    tracer.start_as_current_span.return_value.__enter__.return_value = span

    telemetry = TelemetryService(tracer=tracer, provider=provider)
    telemetry.track_event("simple_event")

    tracer.start_as_current_span.assert_called_once_with("simple_event")
    span.set_attributes.assert_not_called()
