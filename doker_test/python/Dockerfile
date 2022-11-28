FROM python:3.10-slim-bullseye

RUN mkdir app
RUN mkdir -p /datos/datos_ini

COPY ./client_secrets.json /app/

COPY ./modulos/ /app/modulos/

COPY ./datos_ini/ /datos/datos_ini/
COPY .env /app/

WORKDIR /app/
RUN apt-get update
#Installing gcc compiler for psycopg
RUN apt-get install gcc -y 
RUN apt-get install libpq-dev -y
RUN pip install -r requirements.txt


ENTRYPOINT ["python3", "main.py"]
