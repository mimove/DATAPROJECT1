FROM postgres:12.1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install wget -y \
    && apt-get install postgresql-12-postgis-3 -y \
    && apt-get install postgis -y

COPY ./create_tables.sql /docker-entrypoint-initdb.d/

# ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh","postgres"]
