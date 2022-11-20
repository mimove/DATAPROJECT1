import psycopg2

try:
    connection = psycopg2.connect(user="postgres",
                                  password="Welcome01",
                                  host="localhost",
                                  port="5432",
                                  database="idealista")
    cursor = connection.cursor()

    # for i in range(len(dfbarrios)):
        # postgres_insert_query = """ INSERT INTO barrio (id_barrio, nombre, area) VALUES (%s,%s,%s)"""
        # record_to_insert = (dfbarrios['coddistr'][i], dfbarrios['nombre'][i], dfbarrios['areaBarrios'])
        # cursor.execute(postgres_insert_query, record_to_insert)

        # connection.commit()
        # count = cursor.rowcount
        # print(count, "Record inserted successfully into mobile table")

except (Exception, psycopg2.Error) as error:
    print("Unable to connect", error)