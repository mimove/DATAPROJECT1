def insert_data_sql(db:str, table: str, input_df:str, columns: list):
    import psycopg2
    from psycopg2 import sql
    
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="Welcome01",
                                    host="localhost",
                                    port="5432",
                                    database=db)
        cursor = connection.cursor()
        print('Connection done')
        
        
        count = 0
        for i in range(len(input_df)):
            
            # print(barrios_gpd['nombre_barrio'][i])
            
            # postgres_insert_query = """ INSERT INTO barrios (id_barrio, nombre, area) VALUES (%s,%s,%s)"""
            # record_to_insert = (input_df['objectid'][i], input_df['nombre_barrio'][i], input_df['gis_gis_barrios_area'][i])
            # cursor.execute(postgres_insert_query, record_to_insert)

            insertion_query = sql.SQL("INSERT INTO " + table + " VALUES ({})").format(sql.SQL(', ').join(sql.Placeholder()*len(columns)))
            cursor.execute(insertion_query, [str(input_df[columns[j]][i]) if 'POLYGON' in str(input_df[columns[j]][i]) else input_df[columns[j]][i]  for j in range(len(columns))])
                
            
            connection.commit()
            count += cursor.rowcount
        
        print(count, "Records inserted successfully into barrios table") 
        
    except (Exception, psycopg2.Error) as error:
        print("Unable to connect", error)
        
        

def create_caracteristicas_table(db: str):
    import psycopg2
    
    
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="Welcome01",
                                    host="localhost",
                                    port="5432",
                                    database=db)
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO caracteristicas (NOMBRE, DESCRIPCION) VALUES
        ('Transporte Publico', 'Numero estaciones bus y metro'),
        ('Colegios', 'Localizacion colegios'),
        ('Zonas verdes', 'Polígonos con las zonas verdes de Valencia'),
        ('Centros Sanitarios', 'Localizacion de centros sanitarios'),
        ('Contaminacion', 'Nivel de contaminacion'),
        ('Ruido', 'Polígonos con nivel de ruido por cada zona'),
        ('Limpieza','Localizacion de contenedores y papeleras'),
        ('Puntos de recarga', 'Localizacion de puntos de recarga vehiculos eléctricos');
        """
        
        cursor.execute(postgres_insert_query)
        
        connection.commit()
        
        print('Connection done')
    
    except (Exception, psycopg2.Error) as error:
        print("Unable to connect", error)
