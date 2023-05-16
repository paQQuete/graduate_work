FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /opt/fastapi/src
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt -y update && apt -y install netcat && apt -y install kafkacat

EXPOSE 8000
COPY src ./
RUN chmod 777 /opt/src/src/entrypoint.sh
ENTRYPOINT ["/opt/fastapi/src/entrypoint.sh"]

