-- TABLA BARRIOS

create table if not exists barrios (
id_barrio int,
nombre varchar(50) not null,
area float,
constraint pk_barrio primary key (id_barrio)
);