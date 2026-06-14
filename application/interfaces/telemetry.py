from abc import ABC, abstractmethod


class TelemetryPort(ABC):

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
