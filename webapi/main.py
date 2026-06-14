from fastapi import FastAPI

from webapi.container import Container
from webapi.routes import routers


def create_app() -> FastAPI:
    container = Container.create()
    app = FastAPI(title=container.settings.service_name, lifespan=container.lifespan)
    app.state.telemetry_service = container.telemetry_service
    app.state.settings = container.settings
    app.state.health_use_case = container.health_use_case

    for router in routers:
        app.include_router(router)

    return app


app = create_app()
