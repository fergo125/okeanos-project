from layer import *

class LayerColormesh(Layer):
    def __init__(self,var_name,coordinates_x,coordinates_y):
        Layer.__init__(self,var_name,coordinates_x,coordinates_y)
        self.default_params = {'cmap':'k','shading':'interp',\
                                'position':'bottom',\
                                'pad':'0.3',\
                                'vmin':None,\
                                'vmax':None,\
                                'colorbar':"jet",\
                                'units':None,\
                                'segments':None
                                }

    def render(self,map,data,plt):
        if self.default_params['vmin'] is None and self.default_params['vmax'] is None:
            self.default_params['vmin'] = data.min()
            self.default_params['vmax'] = data.max()

        if self.default_params['segments'] is not None:
            mycmap=plt.cm.get_cmap(self.default_params['colorbar'], lut=int(self.default_params["segments"]))
        else:
            mycmap=plt.cm.get_cmap(self.default_params['colorbar'])
        self.colormesh = map.pcolormesh(self.coordinates_x,self.coordinates_y,data.squeeze(),cmap=mycmap,\
        shading=self.default_params['shading'],vmax=float(self.default_params['vmax']),vmin=float(self.default_params['vmin']))
        bar = map.colorbar(self.colormesh,location=self.default_params['position'],pad=float(self.default_params["pad"]))
        bar.ax.tick_params(labelsize=7)
        if self.default_params['units'] is not None:
            bar.ax.set_title(self.default_params['units'],fontsize=7,loc="left")


layer_switcher['colormesh'] = LayerColormesh
