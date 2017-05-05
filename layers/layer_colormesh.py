from layer import *

class LayerColormesh(Layer):
    def __init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector):
        Layer.__init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector)
        self.default_params = {'cmap':'k','shading':'interp','colorbar_location':'bottom'}

    def render_layer(self,map):
        self.colormesh = map.pcolormesh(self.coordinates_vector_x,self.coordinates_vector_y,self.layer_data.squeeze(),cmap=plt.cm.jet,shading='interp')
        bar = map.colorbar(self.colormesh,location='bottom')

layer_switcher['colormesh'] = LayerColormesh
