import uvicorn as uvicorn
from fastapi import FastAPI

# from web.api_v3.endpoints import cadastre as cadastre_api
from web.api_v1 import api_v1


def create_app() -> FastAPI:
    """
    Create application Fast API
    :return:
    """
    app = FastAPI(title='test DOM.RF. Fast API + RabbitMQ + Celery',
                  description='Sample FastAPI Application to demonstrate',
                  version="1.0.0", )

    app.include_router(api_v1)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
