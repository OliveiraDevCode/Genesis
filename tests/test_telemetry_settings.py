from infrastructure.observability.settings import TelemetrySettings


def test_telemetry_settings_use_defaults(monkeypatch):
    monkeypatch.delenv("GENESIS_SERVICE_NAME", raising=False)
    monkeypatch.delenv("GENESIS_TELEMETRY_ENABLED", raising=False)
    monkeypatch.delenv("GENESIS_OTEL_EXPORTER", raising=False)
    monkeypatch.delenv("GENESIS_ENVIRONMENT", raising=False)

    settings = TelemetrySettings.from_environment("GENESIS_WEBAPI")

    assert settings.service_name == "GENESIS_WEBAPI"
    assert settings.enabled is True
    assert settings.exporter == "console"
    assert settings.environment == "development"


def test_telemetry_settings_can_be_configured(monkeypatch):
    monkeypatch.setenv("GENESIS_SERVICE_NAME", "GENESIS_TEST")
    monkeypatch.setenv("GENESIS_TELEMETRY_ENABLED", "false")
    monkeypatch.setenv("GENESIS_OTEL_EXPORTER", "none")
    monkeypatch.setenv("GENESIS_ENVIRONMENT", "test")

    settings = TelemetrySettings.from_environment("GENESIS_WEBAPI")

    assert settings.service_name == "GENESIS_TEST"
    assert settings.enabled is False
    assert settings.exporter == "none"
    assert settings.environment == "test"
