from layer import *

class LayerStream(Layer):
    def __init__(self,var_name,coordinates_x,coordinates_y):
        Layer.__init__(self,var_name,coordinates_x,coordinates_y)
        self.default_params = {'color':'k','stride':"8",'scale':"800",'head_width': 0.04, 'head_length': 0.04, 'width': 0.02,
        'length_includes_head': True}

    def render(self,map,data):
        map.streamplot(self.coordinates_x,self.coordinates_y,data[0],data[1],arrowstyle="<|-")

layer_switcher['stream'] = LayerStream
