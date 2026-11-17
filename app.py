import contextlib
import uvicorn as uvicorn
from fastapi import FastAPI

from web.api_v1 import api_v1
from web.api_v2 import api_v2
from web.api_v3 import api_v3
from database.setup_db import init_db, init_stages, init_priorities
from database.events import register_event_listeners


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Initialize SQLAlchemy event listeners for automatic history tracking
    register_event_listeners()
    # Create tables on a clean database before seeding reference data
    await init_db()
    await init_stages()
    await init_priorities()
    yield


def create_app() -> FastAPI:
    """
    Create application Fast API
    :return:
    """
    app = FastAPI(
        title="test DOM.RF. FastAPI + RabbitMQ + Celery",
        description="Sample FastAPI Application to demonstrate",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(api_v1)
    app.include_router(api_v2)
    app.include_router(api_v3)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
