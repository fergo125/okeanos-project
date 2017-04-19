import layer

layer.layer_switcher[u'contour'] = LayerContour.__init__

class LayerContour(layer.Layer):
    def __init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector):
        layer.Layer.__init__(var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector)

    def render_layer(map):
        map.contour(self.coordinates_vector_x,self.coordinates_vector_y,\
                         self.interp_data.squeeze(),\
                         shading='interp',colors='k',linewidths=0.5)
