## Código main Python del DATA PROJECT 1 EQUIPO: FAN WU, DARIO FERNANDEZ, FRANCISCO ROSILLO Y MIGUEL MORATILLA

import os
import modulos.intersecciones as varinter
import modulos.insert_data_sql as dftosql
import modulos.get_gform_data as getform
import json
import geopandas as gpd
import numpy
import psycopg2


from psycopg2.extensions import register_adapter, AsIs
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client import client, file, tools


print('################################')
print('##    INICIANDO IDEALISTA     ##')
print('################################')



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



# Directorios path

dir_datos_ini = '../datos/datos_ini/'
dir_datos_out = '../datos/datos_out/'



# Carga de datos de barrios

print('Cargando datos barrios')

with open(dir_datos_ini + 'barris-barrios.geojson') as json_file:
    json_data = json.load(json_file)

barrios_json = []
for i in range(len(json_data['features'])):
    barrios_json.append(json_data['features'][i])           # Guardamos campos de geojson




barrios_gpd = gpd.GeoDataFrame.from_features(barrios_json)
barrios_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS
barrios_gpd = barrios_gpd.rename(columns ={'nombre':'nombre_barrio','objectid':'object_id_barrio'}) 


# Lista de características

list_caract = ['%_zona_verde', 'nivel_acustico', 'num_hospitales', 'num_colegios', 'num_chargestations','pm25','num_contenedores','num_transporte']


# Cálculo distribución zonas verdes por barrio

print('Calculando intersección {} con barrios'.format(list_caract[0]))

barrios_caracteristicas = varinter.interseccion_poligonos(barrios_gpd, dir_datos_ini + 'zonas-verdes.geojson', 'area', '',list_caract[0], 3)


# Cálculo distribución acústica por barrio

print('Calculando intersección {} con barrios'.format(list_caract[1]))

barrios_caracteristicas = varinter.interseccion_poligonos(barrios_caracteristicas, dir_datos_ini + 'lday_tota.json', 'count', 'gridcode',list_caract[1], 6)


# Cálculo número de hospitales por barrio

print('Calculando intersección {} con barrios'.format(list_caract[2]))

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'hospitales.geojson',list_caract[2], 'points', 4)


# Cálculo número de centros educativos por barrios

print('Calculando intersección {} con barrios'.format(list_caract[3]))

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'centros-educativos-en-valencia.geojson',list_caract[3], 'points', 2)


# Cálculo número de puntos de carga para coche eléctrico

print('Calculando intersección {} con barrios'.format(list_caract[4]))

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'carregadors-vehicles-electrics-cargadores-vehiculos-electricos.geojson', list_caract[4], 'points', 8)


# Cáculo del nivel de contaminación por barrio

print('Calculando intersección {} con barrios'.format(list_caract[5]))

barrios_caracteristicas = varinter.interpolacion_puntos(barrios_caracteristicas,  dir_datos_ini + 'estacions-contaminacio-atmosferiques-estaciones-contaminacion-atmosfericas.geojson', list_caract[5], 5)



# Cálculo número de contenedores de residuos por barrio

print('Calculando intersección {} con barrios'.format(list_caract[6]))

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'contenidors-residus-solids-contenidores-residuos-solidos.geojson', list_caract[6], 'points', 7)


#Cálculo de estaciones de transporte público por barrios

print('Calculando intersección {} con barrios'.format(list_caract[7]))

barrios_caracteristicas = varinter.interseccion_puntos(barrios_caracteristicas,  dir_datos_ini + 'transporte-barrios.geojson', list_caract[7], 'points', 1)



# Convirtiendo datos Google Form a Pandas y calculando top n preferencias clientes
n = 3
clientes, preferencia_clientes = getform.get_gform_clients('./modulos/responses.xls',list_caract,n)



# Obteniendo pandas con datos para tabla recomendacion

recomendacion_cliente = varinter.inters_preferencias_barrios(barrios_caracteristicas, preferencia_clientes, list_caract,3)



#######################################################

# ## CARGA TABLA CARACTERÍSTICAS EN POSTGRES

# # Inserting values of caracteristicas into table

dftosql.create_caracteristicas_table()


## CARGA TABLA BARRIOS EN POSTGRES

# Ensuring that NaN are transformed to NULL before exporting DataFrame to SQL

barrios_gpd = barrios_gpd.fillna(psycopg2.extensions.AsIs('NULL'))

# Inserting values of barrios into table

dftosql.insert_data_sql('barrios', barrios_gpd, ['object_id_barrio','nombre_barrio','geometry'])




## CARGA TABLA BARRIO-CARACTERÍSTICA EN POSTGRES

# Ensuring that NaN are transformed to NULL before exporting DataFrame to SQL

barrios_caracteristicas = barrios_caracteristicas.fillna(psycopg2.extensions.AsIs('NULL'))

for i in range(len(list_caract)):
    
    # Inserting values of barrios-caracteristicas into table
    
    dftosql.insert_data_sql('barrio_caracteristica', barrios_caracteristicas, ['object_id_barrio','id_caract_' + list_caract[i], list_caract[i]])
    
    

# ## CARGA TABLA CLIENTES EN POSTGRES


## Ensuring that NaN are transformed to NULL before exporting DataFrame to SQL

clientes = clientes.fillna(psycopg2.extensions.AsIs('NULL'))

# Inserting values of clientes into table

dftosql.insert_data_sql('clientes', clientes, ['id_cliente',*[i for i in list_caract]])
 
 

## CARGA TABLA RECOMENDACION EN POSTGRES


# # Ensuring that NaN are transformed to NULL before exporting DataFrame to SQL

recomendacion_cliente = recomendacion_cliente.fillna(psycopg2.extensions.AsIs('NULL'))

# Inserting values of recomendacion_clientes into table

# print(barrios_caracteristicas['date_time'])

# print(recomendacion_cliente['date_time'])

dftosql.insert_data_sql('recomendacion', recomendacion_cliente, ['object_id_barrio','id_cliente','id_caract','date_time'])

 
 
 
# with open("barrios_caracteristicas_final.geojson", "w") as outfile:
#      outfile.write(barrios_caracteristicas.to_json())

