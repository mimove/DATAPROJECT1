-- TABLA BARRIOS

create table if not exists barrios (
    id_barrio int,
    nombre varchar(50) not null,
    area float,
    constraint pk_barrio primary key (id_barrio)
);

CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

ALTER TABLE barrios
ALTER column area type  geometry(polygon,4326);


ALTER TABLE barrios
ADD zona_verde float;


-- TABLA CLIENTES

create table if not exists clientes(
    id_cliente int,
    punt_preg_1 float,
    punt_preg_2 float,
    punt_preg_3 float,
    punt_preg_4 float,
    punt_preg_5 float,
    punt_preg_6 float,
    punt_preg_7 float,
    punt_preg_8 float,
    constraint pk_cliente primary key (id_cliente)
);



-- TABLA RECOMENDACION

create table if not exists recomendacion (
    id_barrio int,
    id_cliente int,
    fecha timestamp,
    constraint pk_recomendacion primary key (id_barrio,id_cliente),
    constraint fk_recomendacion_barrio foreign key (id_barrio) references barrios (id_barrio) ,
    constraint fk_recomendacion_cliente foreign key (id_cliente) references clientes (id_cliente) 
);

-- TABLA DE CARACTERISTICAS

create table if not exists caracteristicas(
    id_caracteristica serial,
    nombre varchar (50),
    descripcion varchar (50),
    constraint pk_caracteristica primary key (id_caracteristica)
);

alter table caracteristicas
alter column descripcion type text;

alter table caracteristicas
alter column nombre type varchar (50);

drop table caracteristicas;

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

alter table barrio_caracteristica
drop constraint  fk_barrio_caract_caracteristica;

select * from barrios;