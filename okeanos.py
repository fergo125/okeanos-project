import untangle
import netCDF4
from netCDF4 import num2date, date2num
import time
import datetime
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
import os
import map_creator
import sys

reload(sys) # just to be sure
sys.setdefaultencoding('utf-8')
params = None
dataset = None

def main():
    xml= open(sys.argv[1],"r").read()
    params = untangle.parse(xml)
    dataset = netCDF4.dataset(params.template.file,"r")
    if params.template['type'] == "gif":
        create_gif()

if __name__=="main":
    main()

def create_gif():
    dataset_vars = list()
    dataset_layers = list()

    latitude_array = dataset[params.template.variables.lat["var_name"]]
    longitude_array = dataset[params.template.variables.lon["var_name"]]

    template_max_longitude = params.template.layers["max_lon"]
    template_max_latitude = params.template.layers["max_lat"]
    template_min_longitude = params.template.layers["min_lon"]
    template_min_latitude = params.template.layers["min_lat"]

    if template_min_latitude >= latitude_array[0] and \
        template_min_longitude >= longitude_array[0] and \
        template_max_latitude <= latitude_array[len(latitude_array)-1] and \
        template_max_latitude <= latitude_array[len(longitude_array)-1]:
        for var in params.template.variables.var:
            dataset_vars.append(dataset[var['var_name']])
        for layer in params.template.layers.layer:
            
    else:
        print('Bad template boundaries')
        return 0
