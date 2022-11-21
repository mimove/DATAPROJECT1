import json
import geopandas as gpd
import matplotlib.pyplot as plt 

import rtree
from descartes import PolygonPatch
import random

def interseccion_poligonos(barrios_in : str, file2 : str, area_count: str, var_to_merge:str, new_column: str):

    ##########################################################
    ## FUNCION QUE CALCULA LA INTERSECCION DE LOS POLIGONOS ##
    ##              DE DOS ARCHIVOS GEOJSON                 ##
    ##########################################################
    
    
    
    barrios_gpd = barrios_in



    with open(file2) as json_file2:
        json_data2 = json.load(json_file2)

    #Cargamos datos del archivo cuyos poligonos queremos intersectar con los de file1

    file2_json=[]

    for i in range(len(json_data2['features'])):
        if json_data2['features'][i]['geometry'] is None:  # Si los datos de geometry que encuentra son NULL pasa a la siguiente linea
            pass
        else:
            file2_json.append(json_data2['features'][i])

    
    file2_gpd = gpd.GeoDataFrame.from_features(file2_json)
    file2_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS

    #CALCULO DE LA INTERSECCION DE POLIGONOS

    merged = gpd.overlay(barrios_gpd, file2_gpd, how = 'intersection') # Calculamos la intersección de los polígonos de barrios con los de el segundo archivo que le pasamos como parametro
    merged.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS

    #GUARDAMOS EL RESULTADO DE LA INTERSECCION EN UN NUEVO ARCHIVO GEOJSON

    # with open("interseccion.geojson", "w") as outfile:
    #     outfile.write(merged.to_json())

    #CARGA DE DATOS CON GPD PARA CALCULAR % DE INTERSECCION

    
    if area_count == 'area':
        
        merged = merged.to_crs("+proj=cea +lat_ts=39.44628964870906 +lon_ts=-0.3326600366971329 +units=km") #Se proyecta sobre el plano para el cálculo adecuado del área

        barrios_gpd = barrios_gpd.to_crs("+proj=cea +lat_ts=39.44628964870906 +lon_ts=-0.3326600366971329 +units=km") #Se proyecta sobre el plano para el cálculo adecuado del área
    
        merged['areaVariable'] = merged.geometry.area #Calculo del área de la intersección de barrios con los poligonos de file2

        barrios_gpd['areaBarrio'] = barrios_gpd.geometry.area #Calculo del area de los barrios

        merged_areas = merged.groupby('nombre_barrio')['areaVariable'].sum() # Sumamos todas las áreas de intersección por barrio
        
        barrios_gpd = barrios_gpd.merge(merged_areas, on='nombre_barrio', how='left') # Hacemos merge de la tabla Barrios con la tabla merged_areas

        barrios_gpd = barrios_gpd.to_crs ('epsg:4326') #Se necesita convertir otra vez a epsg para poder tener las coordenadas GPS correctamente

        
        barrios_gpd[new_column] = barrios_gpd['areaVariable']/barrios_gpd['areaBarrio'] # Obtenemos el % de intersección por cada barrio
        
        barrios_gpd = barrios_gpd.drop(columns=['areaVariable','areaBarrio'])
        
    elif area_count == 'count':   
        
        merged = merged.rename(columns ={var_to_merge:new_column})
                  
        var_merge = merged.groupby('nombre_barrio')[new_column].median()

        barrios_gpd = barrios_gpd.merge(var_merge, on='nombre_barrio', how='left') # Hacemos merge de la tabla Barrios con la tabla var_merge

    

    
    

    #barrios_gpd_pervariable = barrios_gpd.groupby('nombre')['per_variable'].sum() #Sumamos todos los % de area por barrio

    #barrios_gpd_pervariable.to_csv('barrios_pervariable.csv') #Convertimos el dataframe a CSV
    
    return barrios_gpd
    
    


def interseccion_puntos(file1 : str, file2 : str, col: str, type : str):

    #############################################################
    ## FUNCION QUE CALCULA EL NUMERO DE PUNTOS DE UNA VARIABLE ##
    ##                     EN CADA BARRIO                      ##
    #############################################################

    barrios_gpd = file1

    #CARGAMOS DATOS INCIALES DE LOS PUNTOS
    with open(file2) as json_file2:
        json_data2 = json.load(json_file2)

    points_json=[]

    for i in range(len(json_data2['features'])):
        if json_data2['features'][i]['geometry'] is None:  # Si los datos de geometry que encuentra son NULL pasa a la siguiente linea
            pass
        else:  
            points_json.append(json_data2['features'][i])

    #CARGAMOS LOS DATOS CON GEOPANDAS PARA CALCULAR LA INTERSECCION


    points_gpd = gpd.GeoDataFrame.from_features(points_json)
    points_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS


    ## CALCULANDO INTERSECCIÓN BARRIOS CON PUNTOS DE COORDENADAS

    merged = gpd.overlay(barrios_gpd, points_gpd,   how='intersection', keep_geom_type=False) # Calculamos la intersección de los polígonos de barrios con los puntos
    merged.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS

    if type == 'quality':
        merged_quality = gpd.GeoDataFrame(merged['calidad_ambiental'])
        barrios_gpd['calidad_ambiental'] = merged_quality # Hacemos merge de la tabla Barrios con la tabla merged_areas
        barrios_gpd = barrios_gpd.merge(merged_quality, on='calidad_ambiental', how='left')

    elif type == 'points': 
        merged_points = merged.groupby('nombre_barrio')['codigo_barrio'].count().reset_index(name=col) # Sumamos todas las áreas de intersección por barrio

        barrios_gpd = barrios_gpd.merge(merged_points, on='nombre_barrio', how='left') # Hacemos merge de la tabla Barrios con la tabla merged_areas
    
    #print(merged.loc[:,'calidad_ambiental'])



    '''wbr.groupby(["weathersit"]).size()

wbr.loc[(wbr["weathersit"]==1),"ws"]="Sunny"
wbr.loc[(wbr["weathersit"]==2),"ws"]="Cloudy"
wbr.loc[(wbr["weathersit"]==3),"ws"]="Rainy"

wbr.groupby(["ws"]).size()'''

    ## GUARDANDO RESULTADO EN ARCHIVO .geojson
                                              
    # with open(f"interseccion_{col}.geojson", "w") as outfile:
    #     outfile.write(merged.to_json())

    #CARGANDO DATOS CON GEOPANDAS PARA VER LA INTERSECCION

    # do the spatial join, index right is the polygon idx values
    
    # sjoin_gdf = gpd.sjoin(points_gpd, barrios_gpd)
    # sjoin_gdf.crs = 'epsg:4326'

    # # count the values with value counts
    # count_dict = sjoin_gdf['index_right'].value_counts().to_dict()


    # # map the count_dict back to poly_gdf as new point count column 
    # # alternatively you could do a join here, but new col name is nice
    # barrios_gpd[col] = barrios_gpd.index.map(count_dict)

    # #SE CREA LA COLUMNA QUE CUENTA EL NUMERO DE PUNTOS POR BARRIO SEGUN LA VARIABLE
    # barrios_gpd_points = barrios_gpd.groupby('nombre')[col].sum() 

    #SEGUN EL TIPO DE VARIABLE GENERAMOS OUTPUT GEOJSON
    # with open(f"barrios_per{col}.geojson", "w") as outfile:
    #     outfile.write(barrios_gpd.to_json())

    return barrios_gpd