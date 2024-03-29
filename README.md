# DATA PROJECT 1

<p align="center">
<img src="https://datos.gob.es/sites/default/files/styles/success_image/public/success/images/idealista.jpg?itok=uX21SrOq" width=250px>
</p>

## Descripción

El portal lider de compra de vivienda en españa quiere sacar un piloto de calidad de vida aplicado a la vivienda y ha elegido Valencia como sede para su piloto. La idea de este piloto es ofrecer un mapa de calidad de la vivienda en funcion de indicadores de datos abiertos. La calidad de la vivienda se medirá por ruido, hospitales, contaminación… teniendo que dar una nota a una zona en concreto en base a dichos parámetros.

<br>

## Equipo

- [Fan Wu](https://www.linkedin.com/in/fan-wu-98697b13b/): Licenciado en ADE. Encargado de la parte de Business Inteligence y mejora de la aplicación para la incorporación de viviendas a la base de datos a través de Python y POSTRESQL

- [Dario Fernández](https://www.linkedin.com/in/dar%C3%ADo-fern%C3%A1ndez-fern%C3%A1ndez/): Economista. Encargado de la parte de Data Analytics diseñando la encuesta a realizar a los clientes y desarrollando el código para conexión a la API de Google a través de Python

- [Francisco Rosillo](https://www.linkedin.com/in/francisco-rosillo-d%C3%ADez/): Ingeniero de Telecomunicaciones. Parte del equipo de Data Engineering del proyecto. Desarrollo de código Python para carga de base de datos y creación de tablas en POSTGRESQL. También encargado de la parte de Calidad del Dato del proyecto.

- [Miguel Moratilla](https://github.com/mimove): Doctor en Ing. Aeroespacial. Encargado Senior del proyecto. Responsable de la extracción y transformación de los datos desde la web de [open data](https://valencia.opendatasoft.com/pages/home/). Diseño de la arquitectura, y dirección del proyecto distribuyendo tareas entre los componentes del equipo.

<br>

# Diseño de la arquitectura

El proyecto consta de 3 contenedores docker que se encargan de las 3 partes de Data Engineering (ETL) y un cuarto contenedor para realizar un estudio de calidad del dato:

1. Contenedor NiFi (Extracción): el contenedor NiFi se utiliza para la recolección de datos de la web de open data. NiFi se configura a través de un volumen bind mounted en el que se encuentra el flujo que tiene que ser ejecutado automáticamente cuando se levanta el contenedor. Este volumen se está alojado en ./nifi/conf_local. En total se descargan 9 archivos geojson con diferentes datos relativos a la calidad de vida de Valencia. Los archivos son compartidos con el contenedor Python a través de un volumen que se llama nifi_python. Los datos descargados son:

    - Zonas Verdes

    - Distribución de Hospitales

    - Distribución de colegios

    - Nivel de ruido

    - Limpieza

    - Puntos de recarga de coches eléctricos

    - Transporte público



2. Contenedor Python (Transformación): el contenedor Python se encarga de leer los archivos geojson que descarga NiFi, calcular la intersección del geoDataFrame de barrios con todos los geoDataFrame del resto de características, conectarse a la API de Google y calcular los barrios recomendados para los clientes en función de sus respuestas a la encuesta. Una vez hechas todas las transformaciones a los datos, el programa de Python se encarga también de cargar los datos en las tablas de la base de datos SQL. Las funciones creadas se han metido dentro de modulos para tener una estructura más organizada del código. El contenedor tiene 2 volumenes conectados: 

    - nifi_python: Volumen del que recoge los datos descargados por NiFi

    - db_barrios: Volumen en el que escribe el archivo final geojson con las características interpoladas a todos los barrios


3. Contenedor Postgres (Carga): el contenedor Postgres se utiliza como data warehouse para almacenar la base de datos del proyecto. Las tablas se crean desde un archivo .sql en tiempo de construcción del contenedor y son posteriormente alimentadas por Python.


4. Contenedor Jupyter (Calidad del dato): el contenedor docker se conecta a través del volumen db_barrios a python para poder acceder al archivo geojson y realizar un estudio de calidad del dato.

El diagrama con la arquitectura es el siguiente:

<p align="center">
<img src="./.images/docker-compose_test.png" width=500px>
</p>

<br>


Por otro lado, el modelo de datos consta de 6 tablas: Casas, Barrios, Recomendación, Cliente, Barrio_Características y Características, siendo la tabla principal la de Recomendación, ya que es la que unifica la información de los clientes con los barrios que le corresponden para cada característica según el estilo de vida que han respondido en el cuestionario.

<p align="center">
<img src="./.images/DB_image.png" width=500px>
</p>

<br>

## Ejecución del proyecto

Para ejecutar el proyecto simplemente hay que clonar el repositorio y ejecutar*:

```sh
docker compose up
```

Esto levanta todos los contenedores y asigna los volumenes y los puertos a cada uno de ellos. Para ver como funciona el código completo se puede consultar el siguiente video de YouTube:

<https://www.youtube.com/watch?v=w-ZNPGcKnTY&ab_channel=FanWu>



El contenedor NiFi se puede comprobar desde la siguiente dirección:

<http://localhost:8443/nifi>

El contenedor Jupyter se puede comprobar desde la siguiente dirección:

<http://localhost:10000>


Para cargar el archivo en Tableu hay que conectarse a la base de datos con los siguientes campos y abrir el archivo de la carpeta [tableau](./tableau):

| Campo | Texto a completar |
|----------|---------|
| <b>Server Address*</b> | localhost  |
| <b>Port*</b> | 5432  |
| <b>Database*</b> | idealista  |
| <b>Username*</b> | postgres  |
| <b>Password</b> | Welcome01  |



<br>

*El código funciona utilizando la distribución WSL:Ubuntu. Desde Windows existe un problema con el script start.sh de NiFi a la hora de copiarlo al contenedor






