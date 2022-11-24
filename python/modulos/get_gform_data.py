def get_gform_clients(api_form,list_caract):
    
    import pandas as pd
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    # from oauth2client import client, file, tools
    
    
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
    file_obj.GetContentFile('./modulos/responses.xls',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')



    df = pd.read_excel(api_form)

    # df = df.rename(columns={'¿Qué edad tienes?': 'Edad', '¿Tienes hijos?': 'Hijos', '¿Trabajas actualmente?': 'Trabajo', '¿Valoras en gran medida la existencia de comercios cerca de tu zona?': 'Comercios', '¿Valoras en gran medida la existencia de estaciones de transporte público cerca de tu zona?': 'Transporte Publico', '¿Valoras en gran medida la existencia de lugares de ocio cerca de tu zona?': 'Ocio','¿Valoras en gran medida la existencia de colegios cerca de tu zona?': 'Colegios', '¿Valoras en gran medida la existencia de zonas verdes cerca de tu zona?': 'Zonas verdes', '¿Valoras en gran medida la existencia de centros sanitarios cerca de tu zona?': 'Centros Sanitarios', '¿Valoras negativamente la contaminación en tu zona?': 'Contaminacion', '¿El exceso de ruido supone un problema para ti?': 'Ruido', '¿Cuánto valoras la limpieza del barrio?': 'Limpieza','Ante la posibilidad de adquirir un coche electrico, ¿valoras la existencia de puntos de recarga?': 'Puntos de recarga', 'De las comodidades anteriores ¿cuáles serían las 3 que más valoras?': 'Comodidades', '¿Cuánto estarías dispuesto a pagar por el alquiler de una casa que ofrezca todas las comodidades que buscas?': 'Alquiler'})
    dict_caract = {3:'%_zona_verde' , 6:'nivel_acustico', 4:'num_hospitales', 2:'num_colegios', 8:'num_chargestations',5:'pm25',7:'num_contenedores',1:'num_transporte'}
    
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
    
    
    
    
    df = df.drop(['Marca temporal', 'Puntuación','Comercios', 'Trabajo', 'Estado Civil', 'Ocio'], axis=1)

    #adding a column for id
    df.insert(0, 'id_cliente', range(0, len(df)))


    cliente_df = pd.DataFrame()
    cliente_df['id_cliente'] = df['id_cliente']
    cliente_df['Transporte Publico'] = df['Transporte Publico']
    cliente_df['Colegios'] = df['Colegios']
    cliente_df['Zonas verdes'] = df['Zonas verdes']
    cliente_df['Centros Sanitarios'] = df['Centros Sanitarios']
    cliente_df['Contaminacion'] = df['Contaminacion']
    cliente_df['Ruido'] = df['Ruido']
    cliente_df['Limpieza'] = df['Limpieza']
    cliente_df['Puntos de recarga'] = df['Puntos de recarga']
    
    
    caracter_df = pd.DataFrame()

    caracter_df.insert(0, 'id_caract', range(1, len(dict_caract)+1))

    caracter_df['nombre_caract'] = caracter_df['id_caract'].map(dict_caract)

    # print(caracter_df)

    cliente_df = pd.DataFrame()
    cliente_df['id_cliente'] = df['id_cliente']

    for idx, i in enumerate(list_caract):
        cliente_df[i] = df[i]



    top3 = cliente_df.iloc[:, 1:].apply(lambda s: s.abs().nlargest(3).index.tolist(), axis=1) # selecciona el top 3 de preferencias



    preferencia_df = pd.DataFrame()
    preferencia_df['id_cliente'] = cliente_df['id_cliente']
    preferencia_df = preferencia_df.assign(Recomendacion=top3)
    preferencia_df[['Preferencia 1','Preferencia 2', 'Preferencia 3']] = pd.DataFrame(preferencia_df.Recomendacion.tolist(), index= preferencia_df.index)
    preferencia_df = preferencia_df.drop(['Recomendacion'], axis = 1)
    

    preferencia_df = pd.melt(preferencia_df, id_vars=['id_cliente'],
                            value_name="nombre_caract").drop(['variable'],axis=1).sort_values('id_cliente')

    # preferencia_df = preferencia_df.rename(columns ={'Preferencia 1':'nombre'})

    left_merged = pd.merge(
        preferencia_df, caracter_df, how="left", on=['nombre_caract']
    )

    preferencia_df['id_caract'] = left_merged['id_caract']
    
    
    
    return cliente_df, preferencia_df