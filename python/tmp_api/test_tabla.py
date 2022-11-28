import random
import pandas as pd
import json
import psycopg2
import geopandas as gpd
from psycopg2 import sql
from psycopg2.extensions import register_adapter, AsIs

def insert_data_sql(table: str, input_df:str, columns: list):
    import os
    import psycopg2
    from psycopg2 import sql
    
    casas_df = input_df
    # username = os.environ['DB_USER']
    # password = os.environ['DB_PASSWORD']
    # hostname = os.environ['DB_HOST']
    # port = os.environ['DB_PORT']
    # db = os.environ['DB_NAME']
    # username = 'postgres'
    # password = 'Welcome01'
    # hostname = 'localhost'
    # port = 5432
    # db = 'idealista'
    
    
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="Welcome01",
                                    host="localhost",
                                    port=5432,
                                    database="idealista")
        cursor = connection.cursor()
        print('Connection done')
        
        
        count = 0
        for i in range(len(casas_df)):
            
            insertion_query = sql.SQL("INSERT INTO casas VALUES ({})").format(sql.SQL(', ').join(sql.Placeholder()*len(columns)))
            
            
            cursor.execute(insertion_query, [casas_df[columns[j]][i] if 'POINT' in str(casas_df[columns[j]][i]) else casas_df[columns[j]][i]  for j in range(len(columns))])
            
            
            # cursor.execute(insertion_query, [casas_df[columns[j]][i] if 'POINT' in str(casas_df[columns[j]][i]) else casas_df[columns[j]][i]  for j in range(len(columns))])
   
            
            connection.commit()
            count += cursor.rowcount
        
        print(count, "Records inserted successfully into casas table") 
        
    except (Exception, psycopg2.Error) as error:
        print("Unable to connect", error)
        
###################################################################################################################################################################################
############################ MAIN PROGRAM #########################################################################################################################################
###################################################################################################################################################################################

import numpy
from psycopg2.extensions import register_adapter, AsIs
from shapely.geometry import Point

# Crating definition of float and integers for Pandas to SQL

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)

dir_datos_ini = '../../datos/datos_ini/'

with open(dir_datos_ini + 'barris-barrios.geojson') as json_file:
    json_data = json.load(json_file)

barrios_json = []
for i in range(len(json_data['features'])):
    barrios_json.append(json_data['features'][i])           # Guardamos campos de geojson




barrios_gpd = gpd.GeoDataFrame.from_features(barrios_json)




ncasas = 1000

id_casa = list(range(1,ncasas+1))

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
       'name': [i for i in range(ncasas+1)],
       'Lat': [latitude[i] for i in range(len(latitude))],
       'Long': [longitude[i] for i in range(len(longitude))],
       'Price': [price[i] for i in range(len(price))]
      })

gdf1 = gpd.GeoDataFrame(
    df1, geometry=gpd.points_from_xy(df1['Long'], df1['Lat']))

# # for i in final_df['address']:
# #     final_df['address'] = f'POINT{i}'

# # 'str' + df['col'].astype(str)
# final_df['address'] = 'POINT' + final_df['address'].astype(str)

# final_df['address'] = final_df['address'].str.replace(',',' ')


sjoin_gdf= gpd.sjoin(gdf1,barrios_gpd, how="inner")

# sjoin_gdf_table = sjoin_gdf.fillna(psycopg2.extensions.AsIs('NULL'))
# print(final_df)
print(sjoin_gdf)

 
# with open("casas_barrios.geojson", "w") as outfile:
#      outfile.write(sjoin_gdf.to_json())

# connection = psycopg2.connect(user="postgres",
#                             password="Welcome01",
#                             host="localhost",
#                             port=5432,
#                             database="idealista")
# cursor = connection.cursor()
# print('Connection done')

# columns = ['id_casa', 'address']
# count = 0
# for i in range(len(final_df)):
#     insertion_query = """ INSERT INTO casas VALUES (%s,St_PointFromText(%s), %s)"""
#     cursor.execute(insertion_query, [final_df['id_casa'][i], final_df['address'][i], final_df['price'][i]])
#     connection.commit()
#     count += cursor.rowcount









# ALTER TABLE casas
# ALTER column ubicacion type text;