# Changelog

## [BRANCH]
feat/health-endpoint

### Added

- Initial project structure
- FastAPI application
- Health endpoint
- Route registration mechanism
- OpenTelemetry integration
- Application lifecycle management using FastAPI lifespan
- Application startup and shutdown telemetry events
- Basic application logging

### Changed

- Moved health endpoint into dedicated route module
- Separated telemetry configuration from lifecycle events

### Notes

- Genesis can now be started as an HTTP API.
- First endpoint available: GET /health
- Application startup and shutdown are now tracked through telemetry.