from layer import *

class LayerColormesh(Layer):
    def __init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector):
        Layer.__init__(self,var_name,layer_dimensions_indexes,template_lat_vector,template_lon_vector)
        self.default_params = {'cmap':'k','shading':'interp',\
                                'position':'bottom',\
                                'vmin':None,\
                                'vmax':None}

    def render_layer(self,map):
        if self.default_params['vmin'] is None and self.default_params['vmax'] is None:
            self.default_params['vmin'] = self.layer_data.min()
            self.default_params['vmax'] = self.layer_data.max()
        self.colormesh = map.pcolormesh(self.coordinates_vector_x,self.coordinates_vector_y,self.layer_data.squeeze(),cmap=plt.cm.jet,shading='interp')
        bar = map.colorbar(self.colormesh,location=self.default_params['position'])

layer_switcher['colormesh'] = LayerColormesh
