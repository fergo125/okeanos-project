from layer import *

class LayerColormesh(Layer):
    def __init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector):
        Layer.__init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector)
        self.default_params = {'var_u':None,'var_v':None}

    def render_layer(self,map):
        map

    def calculate_u_v(self,data):
        

layer_switcher['colormesh'] = LayerColormesh
