import layer

layer.layer_switcher[u'colormesh'] = LayerContour.__init__

class LayerColormesh(layer.Layer):
    def __init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector):
        layer.Layer.__init__(var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector)

    def render_layer():
        map.pcolormesh(coordinates_vector_x,coordinates_vector_y,interp_data.squeeze(),cmap=plt.cm.jet,shading='interp')
