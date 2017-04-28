import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from layers.layer import Layer,layer_switcher
import os


class MapCreator(object):
    #Cambiar el construcctor para que reciba las medidas del netcdf y ademas las de la plantilla
    def __init__(self,max_lat, max_lon, min_lat, min_lon,precision=None):
        self.map =Basemap(projection='merc',llcrnrlon=min_lon, \
		urcrnrlon=max_lon,llcrnrlat=min_lat,urcrnrlat=max_lat, \
		resolution='c')
        self.layers = list()
        self.template_subindexes = list()
        print("Max_lat: ", max_lat)
        print("Min_lat: ", min_lat)
        print("Precision: ", precision)
        self.lat_vector = np.arange(min_lat,max_lat+precision,precision)
        self.lon_vector = np.arange(min_lon,max_lon+precision,precision)

        self.interpolate_lat_vector = np.linspace(min_lat,max_lat,self.lat_vector.shape[0]*2)
        self.interpolate_lon_vector = np.linspace(min_lon,max_lon,self.lon_vector.shape[0]*2)

        print('lat_vector_template: ', self.lat_vector)
        print('lon_vector_template: ', self.lon_vector)


        #print('lat_vector_interpolate: ', self.interpolate_lat_vector)
        #print('lon_vector_interpolate: ', self.interpolate_lon_vector)


        self.coordinates_vector_x,self.coordinates_vector_y = self.map(*np.meshgrid(self.lon_vector,self.lat_vector))


    #calcular los subindices en el constructor
    def calculate_sub_area(self,lon_vector_data, lat_vector_data,precision):
        base_lat = lat_vector_data.min()
        base_lon = lon_vector_data.min()
        print('Base_lat: ', base_lat)
        print('Base_lon: ', base_lon)
        print('Template max lat: ', self.lat_vector.max())
        print('Template max lon: ', self.lon_vector.max())
        self.template_subindexes.append(int(abs(self.lat_vector.max()-base_lat)/precision))
        self.template_subindexes.append(int(abs(self.lon_vector.max()-base_lon)/precision))
        self.template_subindexes.append(int(abs(self.lat_vector.min()-base_lat)/precision))
        self.template_subindexes.append(int(abs(self.lon_vector.min()-base_lon)/precision))
        print("Sub Indexes: ", self.template_subindexes)

    #hacer que cuando se agregue un nuevo layer se le pase unicamente los datos y los subindices
    def add_layer(self,template_type,var_name):
        #layer = Layer(template_type,var_name,self.template_subindexes,self.lat_vector,self.lon_vector)
        print(layer_switcher)
        new_layer = layer_switcher[template_type](var_name,self.template_subindexes,self.lat_vector,self.lon_vector)
        self.layers.append(new_layer)

        return True
        #self.map.pcolormesh(self.coordinates_vector_x,self.coordinates_vector_y,var_array[0][::-1,::].squeeze(),cmap=plt.cm.jet)
        #plt.show()

    def create_collection(self,var_data,collection_name):
        print('layers',self.layers)
        for data_index in range(0,len(var_data['time'])):
            for layer in self.layers:
                self.map.drawcoastlines()
                self.map.drawcountries()
                self.map.drawmapboundary()
                print('Creating layer', layer.var_name)
                layer.render(self.map,var_data[layer.var_name][data_index][::-1,::],self.interpolate_lat_vector,self.interpolate_lon_vector)
                #self.map.pcolormesh(self.coordinates_vector_x,self.coordinates_vector_y,layer.get_sub_area(var_data[layer.var_name][0][::-1,::]).squeeze(),cmap=plt.cm.jet,shading='interp')
                frame_number = str(data_index)
                save_path = os.path.join(collection_name,collection_name+ frame_number+ '.png')
                print(save_path)
            plt.savefig(save_path)
            plt.close()
        plt.show()
