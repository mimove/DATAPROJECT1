FROM postgres:12.1

# Ponemos el FrontEnd como noninteractive para aceptar automáticamente la primera opción al instalar la librería postgis
# Postgis es necesario para poder definir el tipo de dato GEOMETRY en POSTRESQL

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update \
    && apt-get install wget -y \
    && apt-get install postgresql-12-postgis-3 -y \
    && apt-get install postgis -y

COPY ./create_tables.sql /docker-entrypoint-initdb.d/

