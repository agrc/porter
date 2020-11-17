FROM python:3.8-buster

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update -y && apt-get upgrade -y

RUN ACCEPT_EULA=Y apt-get install unixodbc-dev unixodbc-dev libpq-dev msodbcsql17 -y --no-install-recommends

RUN chmod +rwx /etc/ssl/openssl.cnf
RUN sed -i 's/TLSv1.2/TLSv1/g' /etc/ssl/openssl.cnf
RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/g' /etc/ssl/openssl.cnf

ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY setup.py .
COPY src ./src

RUN python -m pip install -U pip

RUN pip install .[cloud-run]

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 conductor.server:app
