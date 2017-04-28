from layer import *

class LayerContour(Layer):
    def __init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector):
        Layer.__init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector)

    def render_layer(self,map):
        map.contour(self.coordinates_vector_x,self.coordinates_vector_y,\
                         self.layer_data.squeeze(),\
                         shading='interp',colors='k',linewidths=0.5)

layer_switcher['contour'] = LayerContour
