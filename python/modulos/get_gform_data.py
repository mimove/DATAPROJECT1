def get_gform_clients(api_form,list_caract,nprefs):
    
    import pandas as pd
    import time
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive

    
    
    ### Automatic handle of credentials from https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process

    # Initializing a GoogleAuth Object

    gauth = GoogleAuth()


    # Try to load saved client credentials

    gauth.LoadCredentialsFile("./modulos/mycreds.txt")


    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()


    # Save the current credentials to a file

    gauth.SaveCredentialsFile("./modulos/mycreds.txt")
    
    
    # GoogleDrive Instance is created using
    # authenticated GoogleAuth instance

    drive = GoogleDrive(gauth)
    
    # Initialize GoogleDriveFile instance with file id

    file_obj = drive.CreateFile({'id': '15zDrSsGwwX3Kj0oZCPhUPxr0WyRUl1vku6esoxJA7n4'})

    while True:
        try: 
            file_obj.GetContentFile(api_form,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            
            break
        except:
            print('Trying to connect')
            time.sleep(2)


    df = pd.read_excel(api_form)


    # Definición del nº que ocupa cada característica en la Tabla SQL 

    dict_caract = {3:'%_zona_verde' , 6:'nivel_acustico', 4:'num_hospitales', 2:'num_colegios', 8:'num_chargestations',5:'pm25',7:'num_contenedores',1:'num_transporte'}
    


    # Renombramos las columnas que nos vienen de Google Form para tratamiento más sencillo en Python

    df = df.rename(columns={'¿Qué edad tienes?': 'Edad', '¿Tienes hijos?': 'Hijos', '¿Trabajas actualmente?': 'Trabajo', 
                        '¿Valoras en gran medida la existencia de comercios cerca de tu zona?': 'Comercios', 
                        '¿Valoras en gran medida la existencia de estaciones de transporte público cerca de tu zona?': list_caract[7], 
                        '¿Valoras en gran medida la existencia de lugares de ocio cerca de tu zona?': 'Ocio',
                        '¿Valoras en gran medida la existencia de colegios cerca de tu zona?': list_caract[3], 
                        '¿Valoras en gran medida la existencia de zonas verdes cerca de tu zona?': list_caract[0], 
                        '¿Valoras en gran medida la existencia de centros sanitarios cerca de tu zona?': list_caract[2], 
                        '¿Valoras negativamente la contaminación en tu zona?': list_caract[5], 
                        '¿El exceso de ruido supone un problema para ti?': list_caract[1], 
                        '¿Cuánto valoras la limpieza del barrio?': list_caract[6],
                        'Ante la posibilidad de adquirir un coche electrico, ¿valoras la existencia de puntos de recarga?': list_caract[4], 
                        'De las comodidades anteriores ¿cuáles serían las 3 que más valoras?': 'Comodidades', 
                        '¿Cuánto estarías dispuesto a pagar por el alquiler de una casa que ofrezca todas las comodidades que buscas?': 'Alquiler'})
    
    

    # Eliminamos las columnas que, de momento, no utilizamos
    
    df = df.drop(['Marca temporal', 'Puntuación','Comercios', 'Trabajo', 'Estado Civil', 'Ocio'], axis=1)



    # Generamos el ID de cliente

    df.insert(0, 'id_cliente', range(1, len(df)+1))
   
    

    # Dataframe con los datos de las características

    caracter_df = pd.DataFrame()

    caracter_df.insert(0, 'id_caract', range(1, len(dict_caract)+1))

    caracter_df['nombre_caract'] = caracter_df['id_caract'].map(dict_caract)

    
   
    # Dataframe con los datos de los clientes
    cliente_df = pd.DataFrame()
    cliente_df['id_cliente'] = df['id_cliente']



    # Asignamos valores de Dataframe df a Datafram cliente

    for i in list_caract:
        cliente_df[i] = df[i]


    
    top3 = cliente_df.iloc[:, 1:].apply(lambda s: s.abs().nlargest(nprefs).index.tolist(), axis=1) # selecciona el top 3 de preferencias


    # Creamos Dataframe ordenado con las 3 preferencias de cada cliente

    preferencia_df = pd.DataFrame()
    preferencia_df['id_cliente'] = cliente_df['id_cliente']
    preferencia_df = preferencia_df.assign(Recomendacion=top3)
    preferencia_df[['Preferencia ' + str(i+1) for i in range(nprefs)]] = pd.DataFrame(preferencia_df.Recomendacion.tolist(), index= preferencia_df.index)
    preferencia_df = preferencia_df.drop(['Recomendacion'], axis = 1)
    


    # Con el método melt convertimos las columnas de 'Preferencias' en filas para poder hacer un merge con el DataFrame creado en base 
    # a la tabla de la BD características

    preferencia_df = pd.melt(preferencia_df, id_vars=['id_cliente'],
                            value_name="nombre_caract").drop(['variable'],axis=1).sort_values('id_cliente')

    

    preferencia_df = pd.merge(
        preferencia_df, caracter_df, how="left", on=['nombre_caract']
    )

    
    
    return cliente_df, preferencia_df