import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from layers.layer import Layer,layer_switcher
import os


class MapCreator(object):
    #Cambiar el construcctor para que reciba las medidas del netcdf y ademas las de la plantilla
    def __init__(self,max_lat, max_lon, min_lat, min_lon,precision=2):
        self.map =Basemap(projection='merc',llcrnrlon=min_lon, \
		urcrnrlon=max_lon,llcrnrlat=min_lat,urcrnrlat=max_lat, \
		resolution='l')
        self.layers = list()
        self.template_subindexes = list()
        print("Max_lat: ", max_lat)
        print("Min_lat: ", min_lat)
        print("Precision: ", precision)
        self.lat_vector = np.arange(min_lat,max_lat+precision,precision)
        self.lon_vector = np.arange(min_lon,max_lon+precision,precision)

        self.interpolate_lat_vector = np.linspace(min_lat,max_lat,self.lat_vector.shape[0]*1)
        self.interpolate_lon_vector = np.linspace(min_lon,max_lon,self.lon_vector.shape[0]*1)

        print('lat_vector_template: ', self.lat_vector)
        print('lon_vector_template: ', self.lon_vector)

        self.coordinates_vector_x,self.coordinates_vector_y = self.map(*np.meshgrid(self.lon_vector,self.lat_vector))

        self.default_params = {'cmap':'k','shading':'interp',\
                                'position':'bottom',\
                                'vmin':None,\
                                'vmax':None}


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
    def add_layer(self,template_type,var_name,params):
        print(layer_switcher)
        new_layer = layer_switcher[template_type](var_name,self.template_subindexes,self.lat_vector,self.lon_vector)
        new_layer.extra_params(params)
        self.layers.append(new_layer)
        return True

    def add_title(self,title,params):
        new_layer = layer_switcher['title'](title)
        new_layer.extra_params(params)
        self.layers.append(new_layer)

    def set_map_title(self,title,font='Open Sans',size='12'):
        self.title = title
        self.font = font
        self.size = int(size)

    def extra_params():
        pass

    def create_collection(self,var_data,collection_name):

        for data_index in range(0,len(var_data['time'])):
            self.map.drawcoastlines()
            self.map.drawcountries()
            self.map.drawmapboundary()
            self.map.fillcontinents(color=(0.84, 0.82, 0.82))
            self.map.drawmapboundary(fill_color=(0.84, 0.82, 0.82))
            #self.map.drawmeridians(np.arange(self.lon_vector.min(),self.lon_vector.max(),5),labels=[1,0,0,0])
            for layer in self.layers:
                if type(layer) is layer_switcher['title']:
                    layer.render(plt)
                else:
                    print('Creating layer', layer.var_name)
                    layer.render(self.map,var_data[layer.var_name][data_index][::-1],self.interpolate_lat_vector,self.interpolate_lon_vector)
                frame_number = str(data_index)
                save_path = os.path.join(collection_name,collection_name+ frame_number+ '.png')
                print(save_path)
            #plt.axis([self.lon_vector.min(),self.lon_vector.max(),self.lat_vector.min(),self.lat_vector.max()])
            plt.savefig(save_path)
            plt.close()
