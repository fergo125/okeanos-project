from layer import *

class LayerArrows(Layer):
    def __init__(self,var_name,coordinates_x,coordinates_y):
        Layer.__init__(self,var_name,coordinates_x,coordinates_y)
        self.default_params = {'color':'k','stride':"8",'scale':"800"}

    def render(self,map,data):
        #u,v = map.rotate_vector(self.coordinates_x,self.coordinates_y,data[0],data[1])
        map.quiver(self.coordinates_x[::int(self.default_params["stride"]),::int(self.default_params["stride"])],self.coordinates_y[::int(self.default_params["stride"]),::int(self.default_params["stride"])],data[0][::int(self.default_params["stride"]),::int(self.default_params["stride"])]\
                    ,data[1][::int(self.default_params["stride"]),::int(self.default_params["stride"])],color=self.default_params["color"],scale=int(self.default_params["scale"]))

layer_switcher['arrows'] = LayerArrows
