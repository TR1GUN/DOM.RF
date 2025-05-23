import uvicorn as uvicorn
from api import create_app


app = create_app()
celery = app.celery_app


# @app.middleware("http")
# async def add_process_time_header(request, call_next):
#     print('inside middleware!')
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
#     return response


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
