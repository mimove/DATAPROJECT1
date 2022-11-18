## Código main Python del DATA PROJECT 1 EQUIPO: FAN WU, DARIO FERNANDEZ, FRANCISCO ROSILLO Y MIGUEL MORATILLA

import os
import modulos.intersecciones as varinter
import json
import geopandas as gpd


# import rtree


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
barrios_gpd = barrios_gpd.rename(columns ={'nombre':'nombre_barrio','codbarrio':'codigo_barrio'}) 

''''''
barrios_updated = varinter.interseccion_poligonos(barrios_gpd, dir_datos_ini + 'zonas-verdes.geojson', 'area', '','%_zona_verde')


# Cálculo distribución acústica por barrio


barrios_updated = varinter.interseccion_poligonos(barrios_updated, dir_datos_ini + 'lday_tota.json', 'count', 'gridcode','nivel_acustico')


# Cálculo número de hospitales por barrio

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'hospitales.geojson','num_hospitales', 'points' )


# Cálculo número de centros educativos por barrios

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'centros-educativos-en-valencia.geojson','num_colegios', 'points')

 # Cálculo número de puntos de carga para coche eléctrico

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'carregadors-vehicles-electrics-cargadores-vehiculos-electricos.geojson','num_chargestations', 'points')

 # Cáculo número de estaciones de contaminación

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'estacions-contaminacio-atmosferiques-estaciones-contaminacion-atmosfericas.geojson', 'polution_stations', 'quality')

 # Cálculo número de contenedores de residuos por barrio

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'contenidors-residus-solids-contenidores-residuos-solidos.geojson', 'num_contenedores', 'points')

 # Cálculo del numero de papeleras por barrio

barrios_updated = varinter.interseccion_puntos(barrios_updated,  dir_datos_ini + 'papereres-papeleras.geojson', 'num_papeleras', 'points')
 
with open(dir_datos_out + "barrios_updated.geojson", "w") as outfile:  #Generamos archivo geojson con el porventaje de intersección de cada barrio
        outfile.write(barrios_updated.to_json())

