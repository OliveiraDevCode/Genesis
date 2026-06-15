from dataclasses import dataclass, field


@dataclass
class FakeTelemetryService:
    events: list[dict] = field(default_factory=list)

    def track_event(self, name: str, attributes: dict | None = None) -> None:
        self.events.append({"name": name, "attributes": attributes or {}})

    def shutdown(self) -> None:
        pass
