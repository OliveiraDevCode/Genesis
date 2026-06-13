from fastapi import FastAPI

from webapi.routes import routers
from webapi.startup.lifespan import lifespan


app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router)
