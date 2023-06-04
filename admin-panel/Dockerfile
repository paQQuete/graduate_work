FROM python:3.10

WORKDIR /opt/app

RUN apt -y update \
    && apt -y install netcat && apt -y install python-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY run_uwsgi.sh /opt/app/run_uwsgi.sh
COPY requirements.txt /opt/app/requirements.txt
COPY src/uwsgi/uwsgi.ini /opt/app/uwsgi.ini

RUN mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r /opt/app/requirements.txt

EXPOSE 8000
COPY ./src .
RUN chmod 777 /opt/app/static/ && chmod 777 /opt/app/media/
RUN chmod 777 /opt/app/run_uwsgi.sh
