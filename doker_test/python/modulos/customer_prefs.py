import os
import json
import geopandas as gpd
import numpy
import psycopg2
import random
import pandas as pd

def customer_pref(api_form, ):
    df = pd.read_excel(api_form)
