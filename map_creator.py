import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from layers.layer import Layer,layer_switcher
import os


class MapCreator(object):
    #Cambiar el construcctor para que reciba las medidas del netcdf y ademas las de la plantilla
    #def __init__(self,max_lat, max_lon, min_lat, min_lon,precision=2):
    def __init__(self,lat,lon):
        self.map =Basemap(projection='merc',llcrnrlon=lon.min(), \
		urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
		resolution='h')
        self.layers = list()

        self.coordinates_x,self.coordinates_y = self.map(*np.meshgrid(lon,lat))

        self.default_params = {'cmap':'k','shading':'interp',\
                                'position':'bottom',\
                                'vmin':None,\
                                'vmax':None}


    #calcular los subindices en el constructor
    #hacer que cuando se agregue un nuevo layer se le pase unicamente los datos y los subindices
    def add_layer(self,template_type,var_name,params):
        print(layer_switcher)
        new_layer = layer_switcher[template_type](var_name,self.coordinates_x,self.coordinates_y)
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

    def create_collection(self,var_data,collection_name,dpi=200,draw_map=True):
        axis_text = {'fontsize':6}
        coordinates_x,coordinates_y =  self.map(*np.meshgrid(var_data["lon"],var_data["lat"]))
        for data_index in range(0,len(var_data['time'])):
            plt.figure(figsize=(4,4),dpi=170)
            self.map.drawcoastlines()
            if draw_map:
                print("Drawing map")
                self.map.fillcontinents(color="#A0A0A0")
            self.map.drawcountries()
            self.map.drawmapboundary()
            self.map.drawmapboundary(fill_color=(0.84, 0.82, 0.82))
            self.map.drawmeridians(np.linspace(var_data['lon'].min(),var_data['lon'].max(),5)[1:],labels=[0,0,0,1],fontdict=axis_text,color='gray',linewidth=0.5)
            self.map.drawparallels(np.linspace(var_data['lat'].min(),var_data['lat'].max(),5)[1:],labels=[1,0,0,0],fontdict=axis_text,color='gray',linewidth=0.5)
            for layer in self.layers:
                if type(layer) is layer_switcher['title']:
                    layer.render(plt)
                else:
                    layer.render(self.map,var_data[layer.var_name][data_index])
                frame_number = str(data_index)
                save_path = os.path.join(collection_name,collection_name+ frame_number+ '.png')
            print(save_path)
            plt.savefig(save_path,)
            plt.close()
