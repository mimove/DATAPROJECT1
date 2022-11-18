import json
import geopandas as gpd
import matplotlib.pyplot as plt 

import rtree
from descartes import PolygonPatch

def interseccion_poligonos(barrios_in : str, file2 : str, area_count: str, var_to_merge:str, new_column: str):

    ##########################################################
    ## FUNCION QUE CALCULA LA INTERSECCION DE LOS POLIGONOS ##
    ##              DE DOS ARCHIVOS GEOJSON                 ##
    ##########################################################
    
    
    if type(barrios_in) is str:
        
        with open(barrios_in) as json_file:
            json_data = json.load(json_file)

        # Cargamos datos del file1.geojson en una variable solo con las geometría de los polígonos (barrios de Valencia), y en otra con todas las características de cada barrio (coordenadas poligono, nombre barrio, etc.)
        
        barrios_json = []

        for i in range(len(json_data['features'])):
            #Guardamos geometría de los poligonos del geojson
            barrios_json.append(json_data['features'][i])           #Guardamos resto de campos de geojson


        #Carga de datos con Geopandas para calcular la interseccion
        
        barrios_gpd = gpd.GeoDataFrame.from_features(barrios_json)
        barrios_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS
    else:
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

        merged_areas = merged.groupby('nombre')['areaVariable'].sum() # Sumamos todas las áreas de intersección por barrio
        
        barrios_gpd = barrios_gpd.merge(merged_areas, on='nombre', how='left') # Hacemos merge de la tabla Barrios con la tabla merged_areas

        barrios_gpd = barrios_gpd.to_crs ('epsg:4326') #Se necesita convertir otra vez a epsg para poder tener las coordenadas GPS correctamente

        
        barrios_gpd[new_column] = barrios_gpd['areaVariable']/barrios_gpd['areaBarrio'] # Obtenemos el % de intersección por cada barrio
        
        barrios_gpd = barrios_gpd.drop(columns=['areaVariable','areaBarrio'])
        
    elif area_count == 'count':   
        
        merged = merged.rename(columns ={var_to_merge:new_column})
        
        print(merged[new_column])
           
        var_merge = merged.groupby('nombre')[new_column].median()

        barrios_gpd = barrios_gpd.merge(var_merge, on='nombre', how='left') # Hacemos merge de la tabla Barrios con la tabla var_merge

    

    
    

    #barrios_gpd_pervariable = barrios_gpd.groupby('nombre')['per_variable'].sum() #Sumamos todos los % de area por barrio

    #barrios_gpd_pervariable.to_csv('barrios_pervariable.csv') #Convertimos el dataframe a CSV
    
    return barrios_gpd
    
    


def interseccion_puntos(file1 : str, file2 : str):

    #############################################################
    ## FUNCION QUE CALCULA EL NUMERO DE PUNTOS DE UNA VARIABLE ##
    ##                     EN CADA BARRIO                      ##
    #############################################################

    #CARGAMOS LOS DATOS DE LOS BARRIOS
    with open(file1) as json_file:
        json_data = json.load(json_file)

    barrios=[]
    barrios_json = []
    for i in range(len(json_data['features'])):
        barrios.append(json_data['features'][i]['geometry'])    #Guardamos geometría de los poligonos del geojson
        barrios_json.append(json_data['features'][i])           #Guardamos resto de campos de geojson

    #CARGAMOS DATOS INCIALES DE LOS PUNTOS
    with open(file2) as json_file2:
        json_data2 = json.load(json_file2)

    points=[]
    points_json=[]

    for i in range(len(json_data2['features'])):
        if json_data2['features'][i]['geometry'] is None:  # Si los datos de geometry que encuentra son NULL pasa a la siguiente linea
            pass
        else:
            points.append(json_data2['features'][i]['geometry'])   
            points_json.append(json_data2['features'][i])

    #CARGAMOS LOS DATOS CON GEOPANDAS PARA CALCULAR LA INTERSECCION

    barrios_gpd = gpd.GeoDataFrame.from_features(barrios_json)
    barrios_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS
    barrios_gpd.rename(columns ={'nombre':'barrio'}) 


    points_gpd = gpd.GeoDataFrame.from_features(points_json)
    points_gpd.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS


    ## CALCULANDO INTERSECCIÓN BARRIOS CON PUNTOS DE COORDENADAS

    merged = gpd.overlay(barrios_gpd, points_gpd,   how='intersection', keep_geom_type=False) # Calculamos la intersección de los polígonos de barrios con los de zonas verdes
    merged.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS


    ## GUARDANDO RESULTADO EN ARCHIVO .geojson

    with open("interseccion_colegios.geojson", "w") as outfile:
        outfile.write(merged.to_json())


    #CARGANDO DATOS CON GEOPANDAS PARA VER LA INTERSECCION

    # do the spatial join, index right is the polygon idx values
    sjoin_gdf = gpd.sjoin(points_gpd, barrios_gpd)

    # count the values with value counts
    count_dict = sjoin_gdf['index_right'].value_counts().to_dict()


    # map the count_dict back to poly_gdf as new point count column 
    # alternatively you could do a join here, but new col name is nice
    barrios_gpd['point_count'] = barrios_gpd.index.map(count_dict)

    barrios_gpd_points = barrios_gpd.groupby('nombre')['point_count'].sum()

    print(barrios_gpd_points)

    with open("barrios_percolegios.geojson", "w") as outfile:
        outfile.write(barrios_gpd.to_json())
