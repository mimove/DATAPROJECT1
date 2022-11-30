from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client import client, file, tools
import pandas as pd
  
# Initializing a GoogleAuth Object
gauth = GoogleAuth()

# client_secrets.json file is verified
# and it automatically handles authentication
gauth.LocalWebserverAuth()
  
# GoogleDrive Instance is created using
# authenticated GoogleAuth instance
drive = GoogleDrive(gauth)

store = file.Storage('token.json')
creds = store.get()
# Initialize GoogleDriveFile instance with file id
file_obj = drive.CreateFile({'id': '15zDrSsGwwX3Kj0oZCPhUPxr0WyRUl1vku6esoxJA7n4'})
file_obj.GetContentFile('responses.xls',
         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

'''dataframe = pd.read_excel('responses.xls')
print(dataframe)'''




