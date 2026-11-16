#!/bin/bash

# Запуск FastAPI
python app.py &

# Запуск Celery worker
celery -A tasks.celery_app worker --loglevel=info

# Ждать все фоновые процессы
wait
