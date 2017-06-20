from layer import *

class LayerContour(Layer):
    def __init__(self,var_name,coordinates_x,coordinates_y):
        Layer.__init__(self,var_name,coordinates_x,coordinates_y)
        self.default_params = {'colors':'k','shading':'interp','linewidths':'0.5'}

    def render(self,map,data):
        map.contour(self.coordinates_x,self.coordinates_y,\
                         data.squeeze(),\
                         shading=self.default_params['shading'],colors=self.default_params['colors'],linewidths=float(self.default_params['linewidths']))

layer_switcher['contour'] = LayerContour
