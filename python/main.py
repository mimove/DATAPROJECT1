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


barrios_caracteristicas = varinter.interseccion_poligonos(barrios_gpd, dir_datos_ini + 'zonas-verdes.geojson', 'area', '','%_zona_verde', 3)


# Cálculo distribución acústica por barrio


barrios_caracteristicas = varinter.interseccion_poligonos(barrios_caracteristicas, dir_datos_ini + 'lday_tota.json', 'count', 'gridcode','nivel_acustico', 6)


# Cálculo número de hospitales por barrio

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'hospitales.geojson','num_hospitales', 'points', 4)


# Cálculo número de centros educativos por barrios

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'centros-educativos-en-valencia.geojson','num_colegios', 'points', 2)

 # Cálculo número de puntos de carga para coche eléctrico

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'carregadors-vehicles-electrics-cargadores-vehiculos-electricos.geojson','num_chargestations', 'points', 8)

 # Cáculo del nivel de contaminación por barrio

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'estacions-contaminacio-atmosferiques-estaciones-contaminacion-atmosfericas.geojson', 'polution_stations', 'quality', 5)

random_quality = ['Desfavorable', 'Regular', 'Razonablemente buena', 'Buena'] # Declaramos los niveles que obtenemos de los datos

# for i in barrios_caracteristicas['calidad_ambiental']:
    
#     barrios_caracteristicas['calidad_ambiental'] = random.choices(random_quality, k = len(barrios_caracteristicas['calidad_ambiental'])) # Generamos datos random para la calidad ambiental por cada barrio
        
# print(barrios_caracteristicas['calidad_ambiental'])

 # Cálculo número de contenedores de residuos por barrio

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'contenidors-residus-solids-contenidores-residuos-solidos.geojson', 'num_contenedores', 'points', 7)


#Cálculo de estaciones de transporte público por barrios

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'transporte-barrios.geojson', 'num_transporte', 'points', 1)


# with open(dir_datos_out + "barrios_caracteristicas.geojson", "w") as outfile:  #Generamos archivo geojson con el porventaje de intersección de cada barrio
#         outfile.write(barrios_caracteristicas.to_json())
        

# Ensuring that NaN are transformed to NULL before exporting DataFrame to SQL
barrios_gpd = barrios_gpd.fillna(psycopg2.extensions.AsIs('NULL'))


# Inserting values of caracteristicas into table

# dftosql.create_caracteristicas_table('idealista')

# Inserting values of barrios into table

# dftosql.insert_data_sql('idealista', 'barrios', barrios_gpd, ['objectid','nombre_barrio','geometry'])

# print(barrios_gpd['geometry'])



print(barrios_caracteristicas['id_caract'])






        

