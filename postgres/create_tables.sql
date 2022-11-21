-- TABLA BARRIOS

create table barrios (
    id_barrio int,
    nombre varchar(50) not null,
    area float,
    constraint pk_barrio primary key (id_barrio)
);

-- TABLA RECOMENDACION

create table recomendacion (
    id_barrio int,
    id_cliente int,
    fecha datetime,
    constraint fk_barrio foreign key(id_barrio) references barrios(id_barrio)
);

-- TABLA CLIENTES

create table cliente(
    id_cliente int primary key;
    punt_preg_1 float,
    punt_preg_2 float,
    punt_preg_3 float,
    punt_preg_4 float,
    punt_preg_5 float,
    punt_preg_6 float,
    punt_preg_7 float,
    punt_preg_8 float,
    constraint fk_cliente foreign key(id_cliente) references recomendacion(id_cliente)
);

-- TABLA QUE RELACIONA LOS BARRIOS Y LAS CARACTERISTICAS

create table barrio_caracteristica(
    id_barrio int,
    id_caracteristica int,
    puntuacion float,
    fecha datetime,
    constraint fk_barrio foreign key(id_barrio) references barrios(id_barrio)
);

-- TABLA DE CARACTERISTICAS

create table caracteristica(
    id_caracteristica int primary key,
    nombre varchar,
    descripcion varchar (50),
    constraint fk_caracteristica foreign key(id_caracteristica) references barrio_caracteristica(id_caracteristica)
);



