import numpy
import random
import geopandas as gpd
import pandas as pd
from psycopg2.extensions import register_adapter, AsIs



def house_generator(ncasas,barrios_gpd):

    # Crating definition of float and integers for Pandas to SQL



    # def addapt_numpy_float64(numpy_float64):
    #     return AsIs(numpy_float64)
    # def addapt_numpy_int64(numpy_int64):
    #     return AsIs(numpy_int64)
    # register_adapter(numpy.float64, addapt_numpy_float64)
    # register_adapter(numpy.int64, addapt_numpy_int64)


    latitude = []
    longitude = []
    price = []

    # Generate random values as data


    for i in range(ncasas):
        random_latitude = random.uniform(39.390827,39.56145)
        latitude.append(random_latitude)
        random_longtitude = random.uniform(-0.433016,-0.300809)
        longitude.append(random_longtitude)
        random_price = round(random.uniform(300,1400),-1)
        price.append(random_price)

        # # Zip to distribute values into list parentheses units    
        # address_zip = list(zip(longitude,latitude))

        # # print(address_zip)
        # #address = list(address_zip)
        # final_zip = list(zip(id_casa, address_zip,price))
        # #final_list = list(final_zip)


        # # print(final_zip)
        # final_df = pd.DataFrame(final_zip,columns=['id_casa', 'address','price'])

    df1 = pd.DataFrame({
        'id_casa': [i+1 for i in range(ncasas)],
        'Lat': [latitude[i] for i in range(len(latitude))],
        'Long': [longitude[i] for i in range(len(longitude))],
        'price': [price[i] for i in range(len(price))]
        })

    gdf1 = gpd.GeoDataFrame(
        df1, geometry=gpd.points_from_xy(df1['Long'], df1['Lat']))

    gdf1.crs = 'epsg:4326' #Aseguramos que la proyección es la adecuada para coordenadas GPS

    # # for i in final_df['address']:
    # #     final_df['address'] = f'POINT{i}'

    # # 'str' + df['col'].astype(str)
    # final_df['address'] = 'POINT' + final_df['address'].astype(str)

    # final_df['address'] = final_df['address'].str.replace(',',' ')


    sjoin_gdf= gpd.sjoin(gdf1,barrios_gpd, how="left")

    sjoin_gdf = sjoin_gdf.to_crs ('epsg:4326')

    # sjoin_gdf_table = sjoin_gdf.fillna(psycopg2.extensions.AsIs('NULL'))
    # print(final_df)
    # print(sjoin_gdf)

    return sjoin_gdf