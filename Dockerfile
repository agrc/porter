FROM python:3.8-buster

RUN apt-get update && apt-get upgrade && \
  apt-get install unixodbc-dev unixodbc libpq-dev -y --no-install-recommends

ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY setup.py .
COPY src ./src

RUN python -m pip install -U pip

RUN pip install ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 conductor.server:app
