#!/bin/bash

cd /opt/fastapi/src

while ! nc -zv $KAFKABROKER_HOST $KAFKABROKER_PORT; do
      sleep 0.1
      echo "sleep, waiting Kafka Broker  host is up"
done

until kafkacat -L -b ${KAFKABROKER_HOST}:${KAFKABROKER_PORT}; do
    echo "Waiting for Kafka broker to become available..."
    sleep 1
done
echo "Kafka broker is available!"
echo "Ready to start gunicorn"

gunicorn main:app --workers 6 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
