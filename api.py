from fastapi import FastAPI

from endpoints import cadastre as cadastre_api
from celery_tasks.celery.celery_app import create_celery
# app = FastAPI()
# app.include_router(cadastre_api)


def create_app() -> FastAPI:
    """
    Create application Fast API
    :return:
    """
    app = FastAPI(title='test DOM.RF. Fast API + RabbitMQ + Celery',
                  description='Sample FastAPI Application to demonstrate',
                  version="1.0.0", )

    app.celery_app = create_celery()
    app.include_router(cadastre_api)
    return app
