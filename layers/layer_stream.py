from layer import *

class LayerStream(Layer):
    def __init__(self,var_name,coordinates_x,coordinates_y):
        Layer.__init__(self,var_name,coordinates_x,coordinates_y)
        self.default_params = {'color':'k','stride':"8",'scale':"800",'head_width': 0.04, 'head_length': 0.04, 'width': 0.02,
        'length_includes_head': True}

    def render(self,map,data):
        #print("Vectors data:",data)
        #u,v = map.rotate_vector(self.coordinates_x,self.coordinates_y,data[0],data[1])
        map.streamplot(self.coordinates_x,self.coordinates_y,data[0],data[1],arrowstyle="<|-")
        #map.streamplot(self.coordinates_x[0],map(lambda x: x[0],self.coordinates_y),data[0],data[1], latlon=True)
                    #   \, scale=float(self.default_params["scale"]))
                    #headwidth = self.default_params['head_width'], width= self.default_params['width'], headlength = 0.04,)

layer_switcher['stream'] = LayerStream