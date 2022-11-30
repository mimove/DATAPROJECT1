import psycopg2

try:
    connection = psycopg2.connect(user="postgres",
                                  password="Welcome01",
                                  host="localhost",
                                  port="5432",
                                  database="idealista")
    cursor = connection.cursor()
    print('Connection done')
    
    
    # postgreSQL_select_Query = "select * from actor"

    # cursor.execute(postgreSQL_select_Query)
    # print("Selecting rows from mobile table using cursor.fetchall")
    # mobile_records = cursor.fetchall()

    # print("Print each row and it's columns values")
    # for row in mobile_records:
    #     print("Id = ", row[0], )
    #     print("Model = ", row[1])
    #     print("Price  = ", row[2], "\n")
    
    
    # for i in range(len(dfbarrios)):
        # postgres_insert_query = """ INSERT INTO barrio (id_barrio, nombre, area) VALUES (%s,%s,%s)"""
        # record_to_insert = (dfbarrios['coddistr'][i], dfbarrios['nombre'][i], dfbarrios['areaBarrios'])
        # cursor.execute(postgres_insert_query, record_to_insert)

        # connection.commit()
        # count = cursor.rowcount
        # print(count, "Record inserted successfully into mobile table")

except (Exception, psycopg2.Error) as error:
    print("Unable to connect", error)