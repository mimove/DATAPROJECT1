## Código main Python del DATA PROJECT 1 EQUIPO: FAN WU, DARIO FERNANDEZ, FRANCISCO ROSILLO Y MIGUEL MORATILLA

import os
import modulos.intersecciones as varinter

# Ensuring that we're running from the directory of main.py to correctly load the csv files
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


dir_datos_ini = '../datos/datos_ini/'
dir_datos_out = '../datos/datos_out/'

# Cálculo de % area zonas verdes por barrio

# Al ser la primera llamada a la función interseccion_poligonos, pasamos el valor de el archivo barris-barrios.geojson

barrios_updated = varinter.interseccion_poligonos(dir_datos_ini + 'barris-barrios.geojson', dir_datos_ini + 'zonas-verdes.geojson', 'area', '','%_zona_verde')


# Cálculo distribución acústica por barrio

# A partir del segundo valor calculado pasamos ya el geodataframe barrios_updated

barrios_updated = varinter.interseccion_poligonos(barrios_updated, dir_datos_ini + 'lday_tota.json', 'count', 'gridcode','nivel_acustico')





with open(dir_datos_out + "barrios_updated.geojson", "w") as outfile:  #Generamos archivo geojson con el porventaje de intersección de cada barrio
        outfile.write(barrios_updated.to_json())

