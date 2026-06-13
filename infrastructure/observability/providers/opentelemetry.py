from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

from infrastructure.observability.settings import TelemetrySettings


_configured_provider = None


class OpenTelemetry:
    
    def __init__(self, settings: TelemetrySettings):
        self.settings = settings
        self.service_name = settings.service_name
        
    def initialize(self):
        global _configured_provider

        if not self.settings.enabled:
            return self

        if _configured_provider is not None:
            return self
        
        resource = Resource.create(
            {
                "service.name": self.service_name,
                "deployment.environment": self.settings.environment,
            }
        )

        provider = TracerProvider(
            resource=resource
        )

        if self.settings.exporter == "console":
            provider.add_span_processor(
                SimpleSpanProcessor(
                    ConsoleSpanExporter()
                )
            )

        trace.set_tracer_provider(
            provider
        )

        _configured_provider = provider

        return self
        
    def get_tracer(self):
        return trace.get_tracer(self.service_name)

    def shutdown(self):
        if _configured_provider is not None:
            _configured_provider.shutdown()
        
