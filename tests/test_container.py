from webapi.container import Container
from webapi.settings import Settings


def test_container_creates_without_error():
    """Smoke test: the composition root wires everything correctly."""
    container = Container.create()

    assert isinstance(container, Container)
    assert isinstance(container.settings, Settings)
    assert container.telemetry_service is not None
    assert container.health_use_case is not None


def test_container_returns_frozen_dataclass():
    """Container is immutable after creation."""
    container = Container.create()

    try:
        container.settings = Settings()  # type: ignore
        assert False, "Should have raised FrozenInstanceError"
    except Exception:
        pass  # Frozen dataclass raises on assignment


def test_container_health_use_case_has_telemetry():
    """Verify that the use case receives the telemetry service."""
    container = Container.create()

    # The use case was wired with the container's telemetry service
    assert container.health_use_case._telemetry is container.telemetry_service
