import numpy as np
from mpl_toolkits.basemap import interp
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

layer_switcher = dict()

class Layer(object):

    def __init__(self,var_name,coordinates_vector_x,coordinates_vector_y):
        self.coordinates_x= coordinates_vector_x
        self.coordinates_y = coordinates_vector_y
        self.default_params = None
        self.var_name = var_name


    def render(self, map, data):
        pass

    def extra_params(self, params_dict):
        if type(params_dict) is not None:
            for k in self.default_params:
                try:
                    if params_dict[k] is not None:
                        self.default_params[k] = params_dict[k]
                except IndexError or AttributeError:
                    pass
