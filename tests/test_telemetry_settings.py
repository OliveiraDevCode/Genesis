from webapi.settings import Settings


def test_settings_use_defaults(monkeypatch):
    monkeypatch.delenv("GENESIS_SERVICE_NAME", raising=False)
    monkeypatch.delenv("GENESIS_TELEMETRY_ENABLED", raising=False)
    monkeypatch.delenv("GENESIS_OTEL_EXPORTER", raising=False)
    monkeypatch.delenv("GENESIS_ENVIRONMENT", raising=False)

    settings = Settings()

    assert settings.service_name == "genesis"
    assert settings.debug is True
    assert settings.otel_exporter == "console"
    assert settings.environment == "development"


def test_settings_can_be_configured(monkeypatch):
    monkeypatch.setenv("GENESIS_SERVICE_NAME", "genesis-test")
    monkeypatch.setenv("GENESIS_ENVIRONMENT", "test")
    monkeypatch.setenv("GENESIS_OTEL_EXPORTER", "none")
    monkeypatch.setenv("GENESIS_DEBUG", "false")

    settings = Settings()

    assert settings.service_name == "genesis-test"
    assert settings.environment == "test"
    assert settings.otel_exporter == "none"
    assert settings.debug is False
