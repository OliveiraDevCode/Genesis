class TelemetryService:
    
    def __init__(self, tracer, provider):
        self.tracer = tracer
        self._provider = provider
        
    def track_event(self, event_name: str, attributes: dict = None):
        with self.tracer.start_as_current_span(event_name) as span:
            if attributes:
                span.set_attributes(attributes)

    def shutdown(self):
        self._provider.shutdown()