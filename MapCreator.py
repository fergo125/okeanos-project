import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

class MapCreator(object):
    #Cambiar el construcctor para que reciba las medidas del netcdf y ademas las de la plantilla
    def __init__(self,max_lat, max_lon, min_lat, min_lon,precision):
        self.map =Basemap(projection='merc',llcrnrlon=min_lon, \
		urcrnrlon=max_lon,llcrnrlat=min_lat,urcrnrlat=max_lat, \
		resolution='l')
        self.layers = list()
        self.template_subindexes = list()
        lat_vector = np.arange(min_lat,max_lat+precision,precision)
        print('lat_vector_normal: ', lat_vector)
        lon_vector = np.arange(min_lon,max_lon+precision,precision)
        print('lon_vector_normal: ', lon_vector)
        self.coordinates_vector_x,self.coordinates_vector_y = self.map(*np.meshgrid(lon_vector,lat_vector))
        print('lat_vector_coordinates: ', self.coordinates_vector_x)
        print('lon_vector_coordinates: ', self.coordinates_vector_y)
        # self.coordinates_vector_x = lon_vector
        # self.coordinates_vector_y = lat_vector
        self.map.drawcoastlines()
        self.map.drawcountries()
        self.map.drawmapboundary()

    #calcular los subindices en el constructor
    def calculate_sub_indexes(lon_vector_data, lat_vector_data,precision):
        base_lat = self.lat_vector.min()
        base_lon = self.lon_vector.min()

        self.template_subindexes.append((self.lat_vector_data.max()-base_lat)/precision)
        self.template_subindexes.append((self.lon_vector_data.max()-base_lon)/precision)
        self.template_subindexes.append((self.lat_vector_data.min()-base_lat)/precision)
        self.template_subindexes.append((self.lon_vector_data.min()-base_lon)/precision)

    #hacer que cuando se agregue un nuevo layer se le pase unicamente los datos y los subindices
    def add_layer(self,var_array,type):
        #self.map.contour(self.coordinates_vector_x,self.coordinates_vector_y,var_array[0].squeeze(),vmin=0,vmax=0,shading='flat',cmap=plt.cm.jet,latlon=True)
        #self.map.pcolor(self.coordinates_vector_x,self.coordinates_vector_y,var_array[0][-1:0:-1,::].squeeze())
        if len(self.template_subindexes) == 0 :
            calculate_sub_indexes(var_array)
        layer = Layer()

        self.map.pcolormesh(self.coordinates_vector_x,self.coordinates_vector_y,var_array[0][::-1,::].squeeze(),cmap=plt.cm.jet)
        plt.show()
