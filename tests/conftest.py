from dataclasses import dataclass, field

from application.interfaces.telemetry import TelemetryPort


@dataclass
class FakeTelemetryService(TelemetryPort):
    """In-memory fake for TelemetryPort.

    Records all events and exceptions for assertion in tests.
    No OpenTelemetry dependency — fast and deterministic.
    """

    events: list[dict] = field(default_factory=list)
    exceptions: list[dict] = field(default_factory=list)
    _shutdown_called: bool = False

    def track_event(self, name: str, attributes: dict | None = None) -> None:
        self.events.append({"name": name, "attributes": attributes or {}})

    def track_exception(
        self, exception: Exception, attributes: dict | None = None
    ) -> None:
        self.exceptions.append(
            {"exception": exception, "attributes": attributes or {}}
        )

    def shutdown(self) -> None:
        self._shutdown_called = True

    @property
    def shutdown_called(self) -> bool:
        return self._shutdown_called
