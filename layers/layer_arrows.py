from layer import *

class LayerArrows(Layer):
    def __init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector):
        Layer.__init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector)
        self.default_params = {'color':'b'}
    def render_layer(self,map):
        map.quiver(self.coordinates_vector_x,self.coordinates_vector_y,self.layer_data[0],self.layer_data[1],color=default_params["color"])

layer_switcher['arrows'] = LayerArrows
