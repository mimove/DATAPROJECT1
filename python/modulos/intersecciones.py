import json
import geopandas as gpd
import matplotlib.pyplot as plt 
import pandas as pd
import rtree
from descartes import PolygonPatch
import random
import datetime
import time


def interseccion_poligonos(barrios_gpd, file2 : str, area_count: str, var_to_merge:str, new_column: str, id_caract: int):

    ##########################################################
    ## FUNCION QUE CALCULA LA INTERSECCION DE LOS POLIGONOS ##
    ##              DE DOS ARCHIVOS GEOJSON                 ##
    ##########################################################
    
    # Bucle que utilizamos para controlar cuando NiFi ha descargado todos los archivos al volumen que comparte con Python

    while True:
    
        try:
            with open(file2) as json_file2:
                json_data2 = json.load(json_file2)
            break
        except:
            print('Waiting for {} to be copied from NiFi'.format(file2))
            time.sleep(5)


    #Cargamos datos del archivo cuyos poligonos queremos intersectar con los de barrios_gpd

    file2_json=[]

    for i in range(len(json_data2['features'])):
        if json_data2['features'][i]['geometry'] is None:  # Si los datos de geometry que encuentra son NULL pasa a la siguiente linea
            pass
        else:
            file2_json.append(json_data2['features'][i])

    
    file2_gpd = gpd.GeoDataFrame.from_features(file2_json)
    file2_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS
    
    file2_gpd['id_caract'] = id_caract
    
    #CALCULO DE LA INTERSECCION DE POLIGONOS

    merged = gpd.overlay(barrios_gpd, file2_gpd, how = 'intersection') # Calculamos la intersección de los polígonos de barrios con los de el segundo archivo que le pasamos como parametro
    merged.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS




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

    
    # Añadimos el id de la característica como nueva columna al geopandas para intersección
    
    barrios_gpd['id_caract_'+new_column] = id_caract
      
    

    # Añadimos fecha y hora en la que se crea la intersección

    barrios_gpd['date_time'] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
      
    
    return barrios_gpd
    
    


def interseccion_puntos(barrios_gpd, file2 : str, col: str, type : str, id_caract: int):

    #############################################################
    ## FUNCION QUE CALCULA EL NUMERO DE PUNTOS DE UNA VARIABLE ##
    ##                     EN CADA BARRIO                      ##
    #############################################################

    #CARGAMOS DATOS INCIALES DE LOS PUNTOS


    # Bucle que utilizamos para controlar cuando NiFi ha descargado todos los archivos al volumen que comparte con Python

    while True:
    
        try:
            with open(file2) as json_file2:
                json_data2 = json.load(json_file2)
            break
        except:
            print('Waiting for {} to be copied from NiFi'.format(file2))
            time.sleep(5)

    points_json=[]

    for i in range(len(json_data2['features'])):
        if json_data2['features'][i]['geometry'] is None:  # Si los datos de geometry que encuentra son NULL pasa a la siguiente linea
            pass
        else:  
            points_json.append(json_data2['features'][i])



    #CARGAMOS LOS DATOS CON GEOPANDAS PARA CALCULAR LA INTERSECCION

    points_gpd = gpd.GeoDataFrame.from_features(points_json)
    points_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS



    # CALCULANDO INTERSECCIÓN BARRIOS CON PUNTOS DE COORDENADAS

    merged = gpd.overlay(barrios_gpd, points_gpd,   how='intersection', keep_geom_type=False) # Calculamos la intersección de los polígonos de barrios con los puntos
    merged.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS


    if type == 'quality':
        merged_quality = gpd.GeoDataFrame(merged['calidad_ambiental'])
        barrios_gpd['calidad_ambiental'] = merged_quality # Hacemos merge de la tabla Barrios con la tabla merged_areas


    elif type == 'points': 
        merged_points = merged.groupby('nombre_barrio')['object_id_barrio'].count().reset_index(name=col) # Sumamos todas las áreas de intersección por barrio

        barrios_gpd = barrios_gpd.merge(merged_points, on='nombre_barrio', how='left') # Hacemos merge de la tabla Barrios con la tabla merged_areas

    
  
    # Añadimos el id de la característica como nueva columna al geopandas para intersección

    barrios_gpd['id_caract_'+col] = id_caract
    
    barrios_gpd['date_time'] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    

    return barrios_gpd



def interpolacion_puntos(barrios_gpd : str, file2 : str, col: str, id_caract: int):
    

    #CARGAMOS DATOS INCIALES DE LOS PUNTOS
    # Bucle que utilizamos para controlar cuando NiFi ha descargado todos los archivos al volumen que comparte con Python

    while True:
    
        try:
            with open(file2) as json_file2:
                json_data2 = json.load(json_file2)
            break
        except:
            print('Waiting for {} to be copied from NiFi'.format(file2))
            time.sleep(5)

    points_json=[]

    for i in range(len(json_data2['features'])):
        if json_data2['features'][i]['geometry'] is None:  # Si los datos de geometry que encuentra son NULL pasa a la siguiente linea
            pass
        else:  
            points_json.append(json_data2['features'][i])



    #CARGAMOS LOS DATOS CON GEOPANDAS PARA CALCULAR LA INTERSECCION

    points_gpd = gpd.GeoDataFrame.from_features(points_json)
    points_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS
    
    barrios_gpd = barrios_gpd.to_crs("+proj=cea +lat_ts=39.44628964870906 +lon_ts=-0.3326600366971329 +units=km") 
    points_gpd = points_gpd.to_crs("+proj=cea +lat_ts=39.44628964870906 +lon_ts=-0.3326600366971329 +units=km") 


    sjoin_gdf= gpd.sjoin_nearest(barrios_gpd,points_gpd, how="left")

    #Se necesita convertir otra vez a epsg para poder tener las coordenadas GPS correctamente

    # Quitamos valores duplicados del join
    
    sjoin_gdf = sjoin_gdf[~sjoin_gdf['nombre_barrio'].duplicated()]



    # Creamos nueva columan en barrios_gpd con el sjoin de la extrapolación

    barrios_gpd[col] = gpd.GeoDataFrame(sjoin_gdf[col])

    # Aseguramos proyección en coordenadas GPS

    barrios_gpd = barrios_gpd.to_crs ('epsg:4326')

    
    barrios_gpd['id_caract_'+col] = id_caract
    
    barrios_gpd['date_time'] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    
    return barrios_gpd




def inters_preferencias_barrios(barrios_gpd, file2, list_caract,nbarrios):
    
    # Definimos DataFrame para el top nbarrios del cliente

    barrios_top = pd.DataFrame(columns=['object_id_barrio', 'id_caract', 'val_carac','date_time'])

    # Colocamos los valores del top nbarrios obtenidos de barrios_gpd en el nuevo DataFrame

    for i in range(len(list_caract)):
        data = barrios_gpd[['object_id_barrio','id_caract_'+list_caract[i], list_caract[i],'date_time']].sort_values([list_caract[i]], axis = 0, ascending = False).head(nbarrios).values.tolist()
        barrios_top = pd.concat([barrios_top,pd.DataFrame(data, columns=barrios_top.columns)],ignore_index=True)
    
    
    file2 = pd.merge(file2, barrios_top, how="left", on=['id_caract'])
        
    
    return file2





# def interseccion_casas(barrios_gpd, file2 : str, col: str, type : str, id_caract: int):

#     #############################################################
#     ## FUNCION QUE CALCULA EL LAS CASAS QUE SE HAN GENERADO    ##
#     ##       ALEATOREAMENTE Y PERTENECEN A CADA BARRIO         ##
#     #############################################################

    

#     #CARGAMOS DATOS INCIALES DE LOS PUNTOS
#     # Bucle que utilizamos para controlar cuando NiFi ha descargado todos los archivos al volumen que comparte con Python

#     while True:
    
#         try:
#             with open(file2) as json_file2:
#                 json_data2 = json.load(json_file2)
#             break
#         except:
#             print('Waiting for {} to be copied from NiFi'.format(file2))
#             time.sleep(5)

#     points_json=[]

#     for i in range(len(json_data2['features'])):
#         if json_data2['features'][i]['geometry'] is None:  # Si los datos de geometry que encuentra son NULL pasa a la siguiente linea
#             pass
#         else:  
#             points_json.append(json_data2['features'][i])


#     #CARGAMOS LOS DATOS CON GEOPANDAS PARA CALCULAR LA INTERSECCION


#     points_gpd = gpd.GeoDataFrame.from_features(points_json)
#     points_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS


#     ## CALCULANDO INTERSECCIÓN BARRIOS CON PUNTOS DE COORDENADAS

#     merged = gpd.overlay(barrios_gpd, points_gpd,   how='intersection', keep_geom_type=False) # Calculamos la intersección de los polígonos de barrios con los puntos
#     merged.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS

#     if type == 'quality':
#         merged_quality = gpd.GeoDataFrame(merged['calidad_ambiental'])
#         barrios_gpd['calidad_ambiental'] = merged_quality # Hacemos merge de la tabla Barrios con la tabla merged_areas
#         # barrios_gpd = barrios_gpd.merge(merged_quality, on='calidad_ambiental', how='left')

#     elif type == 'points': 
#         merged_points = merged.groupby('nombre_barrio')['object_id_barrio'].count().reset_index(name=col) # Sumamos todas las áreas de intersección por barrio

#         barrios_gpd = barrios_gpd.merge(merged_points, on='nombre_barrio', how='left') # Hacemos merge de la tabla Barrios con la tabla merged_areas

    
    
#     barrios_gpd['id_caract_'+col] = id_caract
    
#     barrios_gpd['date_time'] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")