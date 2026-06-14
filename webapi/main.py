from fastapi import FastAPI

from webapi.container import Container
from webapi.routes import routers


def create_app() -> FastAPI:
    """Build the fully-configured FastAPI application.

    Startup order:
      1. Composition root —— wires all dependencies
      2. FastAPI app     —— with lifespan
      3. Dependencies    —— attached to app.state for FastAPI DI
      4. Routers         —— registered
    """
    container = Container.create()

    app = FastAPI(title=container.settings.service_name, lifespan=container.lifespan)

    # Make dependencies available to FastAPI's Depends() mechanism
    app.state.telemetry_service = container.telemetry_service
    app.state.settings = container.settings
    app.state.health_use_case = container.health_use_case

    for router in routers:
        app.include_router(router)

    return app


# Module-level app instance for uvicorn (uvicorn webapi.main:app)
app = create_app()
