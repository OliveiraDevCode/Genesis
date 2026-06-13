## Learned

### FastAPI Lifecycle

- Difference between import time and startup time.
- FastAPI lifespan is the modern way to handle startup and shutdown.
- Startup and shutdown logic should not be executed during module import.

### Telemetry

- Telemetry configuration should be separated from application lifecycle events.
- APPLICATION_STARTED should be emitted when the application is ready.
- APPLICATION_STOPPED should be emitted during shutdown.
- OpenTelemetry can automatically instrument FastAPI requests.

### Architecture

- main.py should compose the application.
- lifespan.py should manage startup and shutdown.
- telemetry.py should only configure telemetry.
- Shared constants can be reused across layers when they represent application-wide configuration.