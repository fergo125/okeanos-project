from layer import *

class LayerColormesh(Layer):
    def __init__(self,var_name,coordinates_x,coordinates_y):
        Layer.__init__(self,var_name,coordinates_x,coordinates_y)
        self.default_params = {'cmap':'k','shading':'interp',\
                                'position':'bottom',\
                                'vmin':None,\
                                'vmax':None}

    def render(self,map,data):
        if self.default_params['vmin'] is None and self.default_params['vmax'] is None:
            self.default_params['vmin'] = data.min()
            self.default_params['vmax'] = data.max()
        self.colormesh = map.pcolormesh(self.coordinates_x,self.coordinates_y,data.squeeze(),cmap=plt.cm.jet,shading=self.default_params['shading'],vmax=float(self.default_params['vmax']),vmin=float(self.default_params['vmin']))
        bar = map.colorbar(self.colormesh,location=self.default_params['position'])

layer_switcher['colormesh'] = LayerColormesh
