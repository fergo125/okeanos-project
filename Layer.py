import numpy as np
from mpl_toolkits.basemap import interp
import matplotlib.pyplot as plt
class Layer(object):

    def __init__(self,layer_type,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector):
        self.var_name = var_name
        self.layer_type= var_name
        self.lat_vector = template_lat_vector
        self.lon_vector = template_lon_vector
        self.sub_indexes = layer_dimensions_indexes

    def get_sub_area(self, data):
        return data[self.sub_indexes[2]:self.sub_indexes[0]:,\
                            self.sub_indexes[3]:self.sub_indexes[1]:]

    def render(self, map, data, interpolate_lat_vector = None, interpolate_lon_vector = None):
        data_sub_area =  data[self.sub_indexes[2]:self.sub_indexes[0]:,\
                            self.sub_indexes[3]:self.sub_indexes[1]:]
        if interpolate_lat_vector is not None and interpolate_lon_vector is not None:
            print('lat_vector_interpolate shape: ',interpolate_lat_vector.shape)
            print('lon_vector_interpolate shape: ',interpolate_lon_vector.shape)

            lon_interp,lat_interp = np.meshgrid(interpolate_lon_vector,interpolate_lat_vector)
            interp_data = interp(data[self.sub_indexes[2]:self.sub_indexes[0]+1:,self.sub_indexes[3]:self.sub_indexes[1]+1:],\
                                self.lon_vector,self.lat_vector,\
                                lon_interp,lat_interp,order=1)
            coordinates_vector_x,coordinates_vector_y = map(*np.meshgrid(interpolate_lon_vector,interpolate_lat_vector))
            print('Data without interpolation: ', data)
            print('Data interpolated: ' ,interp_data.data)
            print('coordinates_vector_x: ', coordinates_vector_x)
            print('coordinates_vector_y: ', coordinates_vector_y)
            map.pcolormesh(coordinates_vector_x,coordinates_vector_y,interp_data.squeeze(),cmap=plt.cm.jet,shading='interp')
            #map.pcolormesh(interpolate_lon_vector,interpolate_lat_vector,interp_data.squeeze(),cmap=plt.cm.jet,shading='interp',latlon=True)
