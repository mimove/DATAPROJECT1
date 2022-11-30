def house_generator(ncasas,barrios_gpd):

    import numpy
    import random
    import geopandas as gpd
    import pandas as pd
    from psycopg2.extensions import register_adapter, AsIs

    # Definicion listas para almacenar latitud, longitud y precio

    latitude = []
    longitude = []
    price = []


    # Generamos datos aleatorios para las 3 listas

    for i in range(ncasas):
        random_latitude = random.uniform(39.390827,39.56145)
        latitude.append(random_latitude)
        random_longtitude = random.uniform(-0.433016,-0.300809)
        longitude.append(random_longtitude)
        random_price = round(random.uniform(300,1400),-1)
        price.append(random_price)


    # DataFrame con los datos de las casas

    df1 = pd.DataFrame({
        'id_casa': [i+1 for i in range(ncasas)],
        'Lat': [latitude[i] for i in range(len(latitude))],
        'Long': [longitude[i] for i in range(len(longitude))],
        'price': [price[i] for i in range(len(price))]
        })



    # Convertimos a geoDataFrame para intersección con barrios

    gdf1 = gpd.GeoDataFrame(
        df1, geometry=gpd.points_from_xy(df1['Long'], df1['Lat']))

    gdf1.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS

    sjoin_gdf= gpd.sjoin(gdf1,barrios_gpd, how="left")

    sjoin_gdf = sjoin_gdf.to_crs ('epsg:4326') # Definimos coordenadas GPS para la intersección

    return sjoin_gdf