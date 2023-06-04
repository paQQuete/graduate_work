#!/bin/bash

cd /opt/fastapi/src

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
done

gunicorn main:app --workers 6 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
