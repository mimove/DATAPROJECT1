-- TABLA BARRIOS

create table barrios (
id_barrio int,
nombre varchar(50) not null,
area float,
constraint pk_barrio primary key (id_barrio)
);
