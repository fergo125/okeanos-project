from layer import *

class LayerContour(Layer):
    def __init__(self,var_name,coordinates_x,coordinates_y):
        Layer.__init__(self,var_name,coordinates_x,coordinates_y)
        self.default_params = {'colors':'k','shading':'interp','linewidths':'0.5','step':'1','fontsize':'10','labels':'False','fmt':'%1.4f'}

    def render(self,map,data,plt):
        min_data = data.min()
        max_data = data.max()
        contour_levels = np.arange(min_data,max_data,float(self.default_params['step']))
        cs = map.contour(self.coordinates_x,self.coordinates_y,\
                         data.squeeze(),\
                         contour_levels,\
                         shading=self.default_params['shading'],\
                         colors=self.default_params['colors'],\
                         linewidths=float(self.default_params['linewidths']))
        if bool(self.default_params['labels']):
            plt.clabel(cs,fontsize=self.default_params['fontsize'],fmt=self.default_params['fmt'])
    
layer_switcher['contour'] = LayerContour
