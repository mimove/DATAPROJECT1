FROM python:3.10-slim-bullseye

RUN mkdir app
RUN mkdir -p /datos/datos_ini

COPY ./main.py /app/
COPY ./modulos/ /app/modulos/
COPY ./requirements.txt /app/
COPY ./datos_ini/ /datos/datos_ini/
COPY .env /app/

WORKDIR /app/
RUN apt-get update
RUN apt-get install gcc -y
RUN apt-get install libpq-dev -y
RUN pip install -r requirements.txt


ENTRYPOINT ["python3", "main.py"]
