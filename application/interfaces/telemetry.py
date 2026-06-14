from abc import ABC, abstractmethod


class TelemetryPort(ABC):
    """Port for tracking application telemetry events.

    This is the boundary between application use cases and
    the infrastructure that implements telemetry.
    """

    @abstractmethod
    def track_event(self, name: str, attributes: dict | None = None) -> None:
        ...

    @abstractmethod
    def track_exception(
        self, exception: Exception, attributes: dict | None = None
    ) -> None:
        ...

    @abstractmethod
    def shutdown(self) -> None:
        ...
