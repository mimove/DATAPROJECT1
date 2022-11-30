import json
import geopandas as gpd
import matplotlib.pyplot as plt 
import pandas as pd
import rtree
from descartes import PolygonPatch
import random
import datetime
import time


def interseccion_poligonos(barrios_in : str, file2 : str, area_count: str, var_to_merge:str, new_column: str, id_caract: int):

    ##########################################################
    ## FUNCION QUE CALCULA LA INTERSECCION DE LOS POLIGONOS ##
    ##              DE DOS ARCHIVOS GEOJSON                 ##
    ##########################################################
    
    
    
    barrios_gpd = barrios_in



    while True:
    
        try:
            with open(file2) as json_file2:
                json_data2 = json.load(json_file2)
            break
        except:
            print('Waiting for {} to be copied from NiFi'.format(file2))
            time.sleep(5)

    #Cargamos datos del archivo cuyos poligonos queremos intersectar con los de file1

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

    
    
    
    # barrios_gpd['object_id_barrio'] = barrios_in['object_id_barrio']
    
    barrios_gpd['id_caract_'+new_column] = id_caract
      
    
    barrios_gpd['date_time'] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
      
    

    #barrios_gpd_pervariable = barrios_gpd.groupby('nombre')['per_variable'].sum() #Sumamos todos los % de area por barrio

    #barrios_gpd_pervariable.to_csv('barrios_pervariable.csv') #Convertimos el dataframe a CSV
    
    return barrios_gpd
    
    


def interseccion_puntos(file1 : str, file2 : str, col: str, type : str, id_caract: int):

    #############################################################
    ## FUNCION QUE CALCULA EL NUMERO DE PUNTOS DE UNA VARIABLE ##
    ##                     EN CADA BARRIO                      ##
    #############################################################

    barrios_gpd = file1

    #CARGAMOS DATOS INCIALES DE LOS PUNTOS
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


    ## CALCULANDO INTERSECCIÓN BARRIOS CON PUNTOS DE COORDENADAS

    merged = gpd.overlay(barrios_gpd, points_gpd,   how='intersection', keep_geom_type=False) # Calculamos la intersección de los polígonos de barrios con los puntos
    merged.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS

    if type == 'quality':
        merged_quality = gpd.GeoDataFrame(merged['calidad_ambiental'])
        barrios_gpd['calidad_ambiental'] = merged_quality # Hacemos merge de la tabla Barrios con la tabla merged_areas
        # barrios_gpd = barrios_gpd.merge(merged_quality, on='calidad_ambiental', how='left')

    elif type == 'points': 
        merged_points = merged.groupby('nombre_barrio')['object_id_barrio'].count().reset_index(name=col) # Sumamos todas las áreas de intersección por barrio

        barrios_gpd = barrios_gpd.merge(merged_points, on='nombre_barrio', how='left') # Hacemos merge de la tabla Barrios con la tabla merged_areas

    
  
    # barrios_gpd['object_id_barrio'] = file1['object_id_barrio']
    
    barrios_gpd['id_caract_'+col] = id_caract
    
    barrios_gpd['date_time'] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    #print(merged.loc[:,'calidad_ambiental'])


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



def interpolacion_puntos(file1 : str, file2 : str, col: str, id_caract: int):
    
    barrios_gpd = file1

    #CARGAMOS DATOS INCIALES DE LOS PUNTOS
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


    # print(len(sjoin_gdf.index))

    # barrios_gpd.index = merged_quality.index

    barrios_gpd[col] = gpd.GeoDataFrame(sjoin_gdf[col])


    barrios_gpd = barrios_gpd.to_crs ('epsg:4326')
    
    barrios_gpd['id_caract_'+col] = id_caract
    
    barrios_gpd['date_time'] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    
    return barrios_gpd




def inters_preferencias_barrios(file1, file2, list_caract,nbarrios):
    
    barrios_top = pd.DataFrame(columns=['object_id_barrio', 'id_caract', 'val_carac','date_time'])

    for i in range(len(list_caract)):
        data = file1[['object_id_barrio','id_caract_'+list_caract[i], list_caract[i],'date_time']].sort_values([list_caract[i]], axis = 0, ascending = False).head(nbarrios).values.tolist()
        barrios_top = pd.concat([barrios_top,pd.DataFrame(data, columns=barrios_top.columns)],ignore_index=True)
    
    
    file2 = pd.merge(file2, barrios_top, how="left", on=['id_caract'])
        
          
    # file2['object_id_barrio'] = left_merged['object_id_barrio']
    # file2['date_time'] = left_merged['date_time']
    
    
    return file2





def interseccion_casas(file1 : str, file2 : str, col: str, type : str, id_caract: int):

    #############################################################
    ## FUNCION QUE CALCULA EL NUMERO DE PUNTOS DE UNA VARIABLE ##
    ##                     EN CADA BARRIO                      ##
    #############################################################

    barrios_gpd = file1

    #CARGAMOS DATOS INCIALES DE LOS PUNTOS
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


    ## CALCULANDO INTERSECCIÓN BARRIOS CON PUNTOS DE COORDENADAS

    merged = gpd.overlay(barrios_gpd, points_gpd,   how='intersection', keep_geom_type=False) # Calculamos la intersección de los polígonos de barrios con los puntos
    merged.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS

    if type == 'quality':
        merged_quality = gpd.GeoDataFrame(merged['calidad_ambiental'])
        barrios_gpd['calidad_ambiental'] = merged_quality # Hacemos merge de la tabla Barrios con la tabla merged_areas
        # barrios_gpd = barrios_gpd.merge(merged_quality, on='calidad_ambiental', how='left')

    elif type == 'points': 
        merged_points = merged.groupby('nombre_barrio')['object_id_barrio'].count().reset_index(name=col) # Sumamos todas las áreas de intersección por barrio

        barrios_gpd = barrios_gpd.merge(merged_points, on='nombre_barrio', how='left') # Hacemos merge de la tabla Barrios con la tabla merged_areas

    
  
    # barrios_gpd['object_id_barrio'] = file1['object_id_barrio']
    
    barrios_gpd['id_caract_'+col] = id_caract
    
    barrios_gpd['date_time'] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")