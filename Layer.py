import numpy as np
from mpl_toolkits.basemap import interp
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

class Layer(object):

    def __init__(self,layer_type,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector):
        self.var_name = var_name
        self.layer_type= layer_type
        self.lat_vector = template_lat_vector
        self.lon_vector = template_lon_vector
        self.sub_indexes = layer_dimensions_indexes
        self.layer_data = None

    def get_sub_area(self, data):
        return data[self.sub_indexes[2]:self.sub_indexes[0]:,\
                            self.sub_indexes[3]:self.sub_indexes[1]:]
    def interpolate_data(sel,data,datainterpolate_lat_vector, interpolate_lon_vector):
        lon_interp,lat_interp = np.meshgrid(interpolate_lon_vector,interpolate_lat_vector)
        interp_data = interp(data[self.sub_indexes[2]:self.sub_indexes[0]+1:,self.sub_indexes[3]:self.sub_indexes[1]+1:],\
                    self.lon_vector,self.lat_vector,\
                    lon_interp,lat_interp,order=1)
        return interp_data

    def render(self, map, data, interpolate_lat_vector = None, interpolate_lon_vector = None):
        data_sub_area =  data[self.sub_indexes[2]:self.sub_indexes[0]:,\
                            self.sub_indexes[3]:self.sub_indexes[1]:]
        if interpolate_lat_vector is not None and interpolate_lon_vector is not None:
            # print('lat_vector_interpolate shape: ',interpolate_lat_vector.shape)
            # print('lon_vector_interpolate shape: ',interpolate_lon_vector.shape)
            # print('Data to be render',data[self.sub_indexes[2]:self.sub_indexes[0]+1:,self.sub_indexes[3]:self.sub_indexes[1]+1:])
            # lon_interp,lat_interp = np.meshgrid(interpolate_lon_vector,interpolate_lat_vector)
            # interp_data = interp(data[self.sub_indexes[2]:self.sub_indexes[0]+1:,self.sub_indexes[3]:self.sub_indexes[1]+1:],\
            #                     self.lon_vector,self.lat_vector,\
            #                     lon_interp,lat_interp,order=1)
            self.layer_data= interpolate_data
            coordinates_vector_x,coordinates_vector_y = map(*np.meshgrid(interpolate_lon_vector,interpolate_lat_vector))
        else:
            self.layer_data = data
            coordinates_vector_x,coordinates_vector_y = map(*np.meshgrid(interpolate_lon_vector,interpolate_lat_vector))
            # if self.layer_type == 'colormesh':
            #     map.pcolormesh(coordinates_vector_x,coordinates_vector_y,interp_data.squeeze(),cmap=plt.cm.jet,shading='interp')
            # if self.layer_type == 'contour':
            #     print('Contour color', mcolors.to_rgba(mcolors.BASE_COLORS['k']))
            #     map.contour(coordinates_vector_x,coordinates_vector_y,\
            #                 interp_data.squeeze(),\
            #                 shading='interp',colors='k',linewidths=0.5)
            #map.pcolormesh(interpolate_lon_vector,interpolate_lat_vector,interp_data.squeeze(),cmap=plt.cm.jet,shading='interp',latlon=True)

            #Opcion 1:Implementar un metodo que incluya los distintos tipos de parametros necesarios para cada animacion.
            #Opcion 2:Investigar herencia en python y crear distintas clases para cada tipo de visualizacion.
            render_layer()

        def render_layer(self):
            pass
