-- TABLA BARRIOS

CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

create table if not exists barrios (
    id_barrio int,
    nombre varchar(50) not null,
    poligono geometry(polygon,4326),
    constraint pk_barrio primary key (id_barrio)
);



/* ALTER TABLE barrios
ALTER column area type  geometry(polygon,4326); */




-- TABLA CLIENTES

create table if not exists clientes(
    id_cliente int,
    punt_transporte float,
    punt_colegios float,
    punt_zonas_verdes float,
    punt_hospitales float,
    punt_pm25 float,
    punt_ruido float,
    punt_limpieza float,
    punt_puntos_recarga float,
    constraint pk_cliente primary key (id_cliente)
);




-- TABLA DE CARACTERISTICAS

create table if not exists caracteristicas(
    id_caracteristica serial,
    nombre varchar (50),
    descripcion text,
    constraint pk_caracteristica primary key (id_caracteristica)
);



-- TABLA RECOMENDACION (RELACIONA CARACTERISTICAS CON BARRIOS Y CLIENTES SEGÚN SUS PREFERENCIAS)

create table if not exists recomendacion (
    id_barrio int,
    id_cliente int,
    id_caracteristica int,
    fecha timestamp,
    constraint pk_recomendacion primary key (id_barrio,id_cliente),
    constraint fk_recomendacion_barrio foreign key (id_barrio) references barrios (id_barrio) ,
    constraint fk_recomendacion_cliente foreign key (id_cliente) references clientes (id_cliente),
    constraint fk_recomendacion_caracteristica foreign key (id_caracteristica) references caracteristicas (id_caracteristica)
);


-- TABLA QUE RELACIONA LOS BARRIOS Y LAS CARACTERISTICAS

create table if not exists barrio_caracteristica(
    id_barrio int,
    id_caracteristica int,
    puntuacion float,
    fecha timestamp,
    constraint pk_barrio_caracteristica primary key (id_barrio, id_caracteristica),
    constraint fk_barrio_caract_barrios foreign key(id_barrio) references barrios (id_barrio),
    constraint fk_barrio_caract_caracteristica foreign key(id_caracteristica) references caracteristicas (id_caracteristica)
);


