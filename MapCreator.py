import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

class MapCreator(object):
    def __init__(self,max_lat, max_lon, min_lat, min_lon):
        self.map =Basemap(projection='merc',llcrnrlon=min_lon, \
		urcrnrlon=max_lon,llcrnrlat=min_lat,urcrnrlat=max_lat, \
		resolution='h')
        print('template min_lat: ',min_lat)
        print('template min_lon: ',min_lon)
        print('template max_lat: ',max_lat)
        print('template max_lon: ',max_lon)
        lat_vector = np.arange(min_lat,max_lat,0.5)
        print('lat_vector: ', lat_vector)
        lon_vector = np.arange(min_lon,max_lon,0.5)
        print('lon_vector: ', lon_vector)
        self.coordinates_vector_x,self.coordinates_vector_y = self.map(*np.meshgrid(lon_vector,lat_vector))
        self.map.drawcoastlines()
        self.map.drawcountries()
        self.map.drawmapboundary()

    def add_layer(self,var_array,type):
        #self.map.contour(self.coordinates_vector_x,self.coordinates_vector_y,var_array[0].squeeze(),vmin=0,vmax=0,shading='flat',cmap=plt.cm.jet,latlon=True)
        self.map.pcolor(self.coordinates_vector_x,self.coordinates_vector_y,var_array[:][0].squeeze())
        self.map.drawcoastlines()
        plt.show()
