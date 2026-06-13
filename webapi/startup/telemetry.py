import logging
from infrastructure.observability.settings import TelemetrySettings
from infrastructure.observability.services.telemetry import TelemetryService
from infrastructure.shared.constants.logging_constants import LoggingConstants
from infrastructure.observability.providers.opentelemetry import OpenTelemetry
from infrastructure.shared.constants.application_constants import ApplicationConstants


def configure_telemetry():
    logger = logging.getLogger(__name__)

    logger.info(f"{LoggingConstants.STARTUP} Initializing telemetry...")

    settings = TelemetrySettings.from_environment(
        default_service_name=ApplicationConstants.SERVICE_NAME
    )

    provider = OpenTelemetry(settings=settings)
    provider.initialize()

    service = TelemetryService(provider.get_tracer(), provider)

    logger.info(f"{LoggingConstants.TELEMETRY} Telemetry initialized successfully")

    return service