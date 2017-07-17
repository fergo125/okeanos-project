from layer import *

class LayerArrows(Layer):
    def __init__(self,var_name,coordinates_x,coordinates_y):
        Layer.__init__(self,var_name,coordinates_x,coordinates_y)
        self.default_params = {'color':'k','stride_lat':"8",'stride_lon':"8",'scale':"800",'head_width': 0.04, 'head_length': 0.04, 'width': 0.02,
        'length_includes_head': True}

    def render(self,map,data):
        #print("Vectors data:",data)
        #u,v = map.rotate_vector(self.coordinates_x,self.coordinates_y,data[0],data[1])
        map.quiver(self.coordinates_x[int(self.default_params["stride_lon"])::int(self.default_params["stride_lon"]),int(self.default_params["stride_lat"])::int(self.default_params["stride_lat"])],\
                   self.coordinates_y[int(self.default_params["stride_lon"])::int(self.default_params["stride_lon"]),int(self.default_params["stride_lat"])::int(self.default_params["stride_lat"])],\
                   data[0][int(self.default_params["stride_lon"])::int(self.default_params["stride_lon"]),int(self.default_params["stride_lat"])::int(self.default_params["stride_lat"])],\
                   data[1][int(self.default_params["stride_lon"])::int(self.default_params["stride_lon"]),int(self.default_params["stride_lat"])::int(self.default_params["stride_lat"])],color=self.default_params["color"],units="inches")
                    #   \, scale=float(self.default_params["scale"]))
                    #headwidth = self.default_params['head_width'], width= self.default_params['width'], headlength = 0.04,)

layer_switcher['arrows'] = LayerArrows
