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



list_caract = ['%_zona_verde', 'nivel_acustico', 'num_hospitales', 'num_colegios', 'num_chargestations','polution_stations','num_contenedores','num_transporte']

# Cálculo distribución zonas verdes por barrio


barrios_caracteristicas = varinter.interseccion_poligonos(barrios_gpd, dir_datos_ini + 'zonas-verdes.geojson', 'area', '',list_caract[0], 3)


# # # Cálculo distribución acústica por barrio


barrios_caracteristicas = varinter.interseccion_poligonos(barrios_caracteristicas, dir_datos_ini + 'lday_tota.json', 'count', 'gridcode',list_caract[1], 6)


# # Cálculo número de hospitales por barrio

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'hospitales.geojson',list_caract[2], 'points', 4)


# # Cálculo número de centros educativos por barrios

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'centros-educativos-en-valencia.geojson',list_caract[3], 'points', 2)

#  # Cálculo número de puntos de carga para coche eléctrico

#barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'carregadors-vehicles-electrics-cargadores-vehiculos-electricos.geojson', list_caract[4], 'points', 8)

#  # Cáculo del nivel de contaminación por barrio

# barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'estacions-contaminacio-atmosferiques-estaciones-contaminacion-atmosfericas.geojson', list_caract[5], 'quality', 5)

# random_quality = ['Desfavorable', 'Regular', 'Razonablemente buena', 'Buena'] # Declaramos los niveles que obtenemos de los datos

# for i in barrios_caracteristicas['calidad_ambiental']:
    
#     barrios_caracteristicas['calidad_ambiental'] = random.choices(random_quality, k = len(barrios_caracteristicas['calidad_ambiental'])) # Generamos datos random para la calidad ambiental por cada barrio
        
# # print(barrios_caracteristicas['calidad_ambiental'])

# # Cálculo número de contenedores de residuos por barrio

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'contenidors-residus-solids-contenidores-residuos-solidos.geojson', list_caract[6], 'points', 7)


# #Cálculo de estaciones de transporte público por barrios

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'transporte-barrios.geojson', list_caract[7], 'points', 1)


# # with open(dir_datos_out + "barrios_caracteristicas.geojson", "w") as outfile:  #Generamos archivo geojson con el porventaje de intersección de cada barrio
# #         outfile.write(barrios_caracteristicas.to_json())
        

# # Ensuring that NaN are transformed to NULL before exporting DataFrame to SQL
# barrios_gpd = barrios_gpd.fillna(psycopg2.extensions.AsIs('NULL'))


# Inserting values of caracteristicas into table

# dftosql.create_caracteristicas_table('idealista')

# Inserting values of barrios into table

# dftosql.insert_data_sql('idealista', 'barrios', barrios_gpd, ['objectid','nombre_barrio','geometry'])

# print(barrios_gpd['geometry'])


# Ensuring that NaN are transformed to NULL before exporting DataFrame to SQL
barrios_caracteristicas = barrios_caracteristicas.fillna(psycopg2.extensions.AsIs('NULL'))

for i in range(len(list_caract)):
    dftosql.insert_data_sql('idealista', 'barrio_caracteristica', barrios_caracteristicas, ['object_id_barrio','id_caract_' + list_caract[i], list_caract[i]])
    

# print(barrios_caracteristicas['object_id_barrio'])

# print(barrios_caracteristicas['id_caract_nivel_acustico'])



# print(barrios_caracteristicas)


        

