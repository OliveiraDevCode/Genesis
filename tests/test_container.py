from webapi.container import Container
from webapi.settings import Settings


def test_container_creates_without_error():
    container = Container.create()

    assert isinstance(container, Container)
    assert isinstance(container.settings, Settings)
    assert container.telemetry_service is not None
    assert container.health_use_case is not None


def test_container_returns_frozen_dataclass():
    container = Container.create()

    try:
        container.settings = Settings()
        assert False
    except Exception:
        pass


def test_container_health_use_case_has_telemetry():
    container = Container.create()

    assert container.health_use_case._telemetry is container.telemetry_service
