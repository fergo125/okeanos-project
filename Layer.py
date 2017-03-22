class Layer(object):

    def __init__(self,layer_type,var_name,layer_dimensions_indexes):
        self.var_name = var_name
        self.layer_type= var_name
        self.sub_indexes = layer_dimensions_indexes

    def get_sub_area(self, data):
        return data[self.sub_indexes[2]:self.sub_indexes[0]:,\
                            self.sub_indexes[3]:self.sub_indexes[1]:]
    def render(self, map, data):
        data_sub_area =  data[self.sub_indexes[2]:self.sub_indexes[0]:,\
                            self.sub_indexes[3]:self.sub_indexes[1]:]
