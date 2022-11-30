def insert_data_sql(table: str, input_df:str, columns: list):

    import os
    import psycopg2
    from psycopg2 import sql
    
    #########################
    ## Definición de variables cuando se utiliza el código main.py python dockerizado

    username = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    hostname = os.environ['DB_HOST']
    port = os.environ['DB_PORT']
    db = os.environ['DB_NAME']
    
    
    #########################
    ## Definición de variables cuando se utiliza el código main.py python sin dockerizar

    # username = 'postgres'
    # password = 'Welcome01'
    # hostname = 'localhost'
    # port = 5432
    # db = 'idealista'
    
    
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=hostname,
                                    port=port,
                                    database=db)
        cursor = connection.cursor()
        print('Connection done')
        
        
        count = 0
        for i in range(len(input_df)):

            # Definición de query con el nº de columnas que queremos insertar

            insertion_query = sql.SQL("INSERT INTO " + table + " VALUES ({})").format(sql.SQL(', ').join(sql.Placeholder()*len(columns)))
            

            # Insertamos los valores que nos vienen desde el geoDataFrame que llamamos en la función. El list comprehension se utiliza para generar una lista en una sola
            # linea con las condiciones if de detectar si la columna es del tipo "geometry" y si tiene en ese columna polígonos o puntos
             
            cursor.execute(insertion_query, [str(input_df[columns[j]][i]) if any(c in str(input_df[columns[j]][i]) for c in ('POLYGON','POINT')) else input_df[columns[j]][i] for j in range(len(columns))])

            
            connection.commit()
            count += cursor.rowcount
        
        print(count, "Records inserted successfully into " + table + " table") 
        
    except (Exception, psycopg2.Error) as error:
        print("Unable to connect", error)
        
        

def create_caracteristicas_table():
    import os
    import psycopg2
    

    #########################
    ## Definición de variables cuando se utiliza el código main.py python dockerizado
    
    username = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    hostname = os.environ['DB_HOST']
    port = os.environ['DB_PORT']
    db = os.environ['DB_NAME']
    

    #########################
    ## Definición de variables cuando se utiliza el código main.py python sin dockerizar
    
    # username = 'postgres'
    # password = 'Welcome01'
    # hostname = 'localhost'
    # port = 5432
    # db = 'idealista'
    
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=hostname,
                                    port=port,
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
        
        print('Table caracteristicas filled')
    
    except (Exception, psycopg2.Error) as error:
        print("Unable to connec", error)
