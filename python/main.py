## Código main Python del DATA PROJECT 1 EQUIPO: FAN WU, DARIO FERNANDEZ, FRANCISCO ROSILLO Y MIGUEL MORATILLA

import os
import modulos.intersecciones as varinter
import modulos.insert_data_sql as dftosql
import json
import geopandas as gpd
import numpy
import psycopg2
import random

from psycopg2.extensions import register_adapter, AsIs


# Crating definition of float and integers for Pandas to SQL
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)



# Ensuring that we're running from the directory of main.py to correctly load the csv files
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)




dir_datos_ini = '../datos/datos_ini/'
dir_datos_out = '../datos/datos_out/'




# Cálculo de % area zonas verdes por barrio

# Al ser la primera llamada a la función interseccion_poligonos, pasamos el valor de el archivo barris-barrios.geojson

#CARGAMOS LOS DATOS DE LOS BARRIOS
with open(dir_datos_ini + 'barris-barrios.geojson') as json_file:
    json_data = json.load(json_file)

barrios_json = []
for i in range(len(json_data['features'])):
    barrios_json.append(json_data['features'][i])           #Guardamos resto de campos de geojson


barrios_gpd = gpd.GeoDataFrame.from_features(barrios_json)
barrios_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS
barrios_gpd = barrios_gpd.rename(columns ={'nombre':'nombre_barrio','objectid':'object_id_barrio'}) 



# Cálculo distribución zonas verdes por barrio


barrios_updated = varinter.interseccion_poligonos(barrios_gpd, dir_datos_ini + 'zonas-verdes.geojson', 'area', '','%_zona_verde')


# Cálculo distribución acústica por barrio


barrios_updated = varinter.interseccion_poligonos(barrios_updated, dir_datos_ini + 'lday_tota.json', 'count', 'gridcode','nivel_acustico')


# Cálculo número de hospitales por barrio

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'hospitales.geojson','num_hospitales', 'points' )


# Cálculo número de centros educativos por barrios

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'centros-educativos-en-valencia.geojson','num_colegios', 'points')

 # Cálculo número de puntos de carga para coche eléctrico

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'carregadors-vehicles-electrics-cargadores-vehiculos-electricos.geojson','num_chargestations', 'points')

 # Cáculo del nivel de contaminación por barrio

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'estacions-contaminacio-atmosferiques-estaciones-contaminacion-atmosfericas.geojson', 'polution_stations', 'quality')

random_quality = ['Desfavorable', 'Regular', 'Razonablemente buena', 'Buena'] # Declaramos los niveles que obtenemos de los datos

for i in barrios_updated['calidad_ambiental']:
    
    barrios_updated['calidad_ambiental'] = random.choices(random_quality, k = len(barrios_updated['calidad_ambiental'])) # Generamos datos random para la calidad ambiental por cada barrio
        
print(barrios_updated['calidad_ambiental'])

 # Cálculo número de contenedores de residuos por barrio

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'contenidors-residus-solids-contenidores-residuos-solidos.geojson', 'num_contenedores', 'points')

 # Cálculo del numero de papeleras por barrio

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'papereres-papeleras.geojson', 'num_papeleras', 'points')

# Calculo numero estaciones metro

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'fgv-estacions-estaciones.geojson', 'num_estaciones', 'points')

 #Cálculo de estaciones de transporte público por barrios

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'transporte-barrios.geojson', 'num_transporte', 'points')


with open(dir_datos_out + "barrios_updated.geojson", "w") as outfile:  #Generamos archivo geojson con el porventaje de intersección de cada barrio
        outfile.write(barrios_updated.to_json())
        

# Ensuring that NaN are transformed to NULL before exporting DataFrame to SQL
barrios_gpd = barrios_gpd.fillna(psycopg2.extensions.AsIs('NULL'))




# Inserting values of barrios into table

dftosql.insert_data_sql('idealista', 'barrios', barrios_gpd, ['objectid','nombre_barrio','geometry'])

# print(barrios_gpd['geometry'])








# try:
#     connection = psycopg2.connect(user="postgres",
#                                 password="Welcome01",
#                                 host="localhost",
#                                 port="5432",
#                                 database="idealista")
#     cursor = connection.cursor()
#     print('Connection done')
     
#     count = 0
#     for i in range(len(barrios_gpd)):
        
#         # print(barrios_gpd['nombre_barrio'][i])
         
#         postgres_insert_query = """ INSERT INTO barrios (id_barrio, nombre, area) VALUES (%s,%s,%s)"""
#         record_to_insert = (barrios_gpd['objectid'][i], barrios_gpd['nombre_barrio'][i], barrios_gpd['gis_gis_barrios_area'][i])
#         cursor.execute(postgres_insert_query, record_to_insert)

#         connection.commit()
#         count += cursor.rowcount
        
#     print(count, "Records inserted successfully into barrios table")
    


# except (Exception, psycopg2.Error) as error:
#     print("Unable to connect", error)


        

