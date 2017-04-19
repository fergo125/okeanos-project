import numpy as np
from mpl_toolkits.basemap import interp
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

layer_switcher = dict()

class Layer(object):

    def __init__(self,layer_type,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector):
        self.var_name = var_name
        #self.layer_type= layer_type
        self.lat_vector = template_lat_vector
        self.lon_vector = template_lon_vector
        self.sub_indexes = layer_dimensions_indexes
        self.layer_data = None
        self.coordinates_vector_x= None
        self.coordinates_vector_y = None

    def get_sub_area(self, data):
        return data[self.sub_indexes[2]:self.sub_indexes[0]:,\
                            self.sub_indexes[3]:self.sub_indexes[1]:]
    def interpolate_data(self,data,datainterpolate_lat_vector, interpolate_lon_vector):
        lon_interp,lat_interp = np.meshgrid(interpolate_lon_vector,interpolate_lat_vector)
        interp_data = interp(data[self.sub_indexes[2]:self.sub_indexes[0]+1:,self.sub_indexes[3]:self.sub_indexes[1]+1:],\
                    self.lon_vector,self.lat_vector,\
                    lon_interp,lat_interp,order=1)
        return interp_data

    def render(self, map, data, interpolate_lat_vector = None, interpolate_lon_vector = None):
        data_sub_area =  data[self.sub_indexes[2]:self.sub_indexes[0]:,\
                            self.sub_indexes[3]:self.sub_indexes[1]:]
        if interpolate_lat_vector is not None and interpolate_lon_vector is not None:
            self.layer_data= interpolate_data
            self.coordinates_vector_x,self.coordinates_vector_y = map(*np.meshgrid(interpolate_lon_vector,interpolate_lat_vector))
        else:
            self.layer_data = data
            self.coordinates_vector_x,self.coordinates_vector_y = map(*np.meshgrid(interpolate_lon_vector,interpolate_lat_vector))

            #Opcion 1:Implementar un metodo que incluya los distintos tipos de parametros necesarios para cada animacion.
            #Opcion 2:Investigar herencia en python y crear distintas clases para cada tipo de visualizacion.
        render_layer()

        def render_layer(self,map):
            pass
