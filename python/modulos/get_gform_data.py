def get_gform_clients():
    
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



    df = pd.read_excel('./modulos/responses.xls')

    df = df.rename(columns={'¿Qué edad tienes?': 'Edad', '¿Tienes hijos?': 'Hijos', '¿Trabajas actualmente?': 'Trabajo', '¿Valoras en gran medida la existencia de comercios cerca de tu zona?': 'Comercios', '¿Valoras en gran medida la existencia de estaciones de transporte público cerca de tu zona?': 'Transporte Publico', '¿Valoras en gran medida la existencia de lugares de ocio cerca de tu zona?': 'Ocio','¿Valoras en gran medida la existencia de colegios cerca de tu zona?': 'Colegios', '¿Valoras en gran medida la existencia de zonas verdes cerca de tu zona?': 'Zonas verdes', '¿Valoras en gran medida la existencia de centros sanitarios cerca de tu zona?': 'Centros Sanitarios', '¿Valoras negativamente la contaminación en tu zona?': 'Contaminacion', '¿El exceso de ruido supone un problema para ti?': 'Ruido', '¿Cuánto valoras la limpieza del barrio?': 'Limpieza','Ante la posibilidad de adquirir un coche electrico, ¿valoras la existencia de puntos de recarga?': 'Puntos de recarga', 'De las comodidades anteriores ¿cuáles serían las 3 que más valoras?': 'Comodidades', '¿Cuánto estarías dispuesto a pagar por el alquiler de una casa que ofrezca todas las comodidades que buscas?': 'Alquiler'})
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
    
    
    return cliente_df