
# data = gpd.read_file("/home/ttmam/GitHub/DATAPROJECT1/datos_ini/barris-barrios.geojson")

from matplotlib import pyplot
from descartes import PolygonPatch
import math
# import urllib2
import simplejson
import json

data = []

with open('/home/ttmam/GitHub/DATAPROJECT1/datos_ini/barris-barrios.geojson') as json_file:
    json_data = json.load(json_file)


print(json_data.keys())

poly=[]
for i in range(len(json_data['features'])):
    poly.append(json_data['features'][i]['geometry'])

print(poly)

""" import matplotlib.pyplot as plt 
from descartes import PolygonPatch
BLUE = '#6699cc'
fig = plt.figure() 
ax = fig.gca() 
ax.add_patch(PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2 ))
ax.axis('scaled')
plt.show() """




""" def plotFeature(coordlist, myplot):
    #create a polygon geojson-like feature
    poly = {"type": "Polygon", "coordinates": coordlist}
    patch = PolygonPatch(poly, fc='#6699cc', ec='#6699cc', alpha=0.5, zorder=2)
    #plot it on the graph
    myplot.add_patch(patch)
 """

""" for coordlist in data['features'][0]['geometry']['coordinates']:
    plotFeature(coordlist, myplot)

fig = pyplot.figure(1, figsize=(10, 4), dpi=180) """