from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import os
import json
import geopandas as gpd

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Initializing a GoogleAuth Object
gauth = GoogleAuth()
  
# client_secrets.json file is verified
# and it automatically handles authentication
gauth.LocalWebserverAuth()
  
# GoogleDrive Instance is created using
# authenticated GoogleAuth instance
drive = GoogleDrive(gauth)
  
# Initialize GoogleDriveFile instance with file id
file_obj = drive.CreateFile({'id': '15zDrSsGwwX3Kj0oZCPhUPxr0WyRUl1vku6esoxJA7n4'})
file_obj.GetContentFile('responses.xls',
         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  
dataframe = pd.read_excel('responses.xls')
print(dataframe)