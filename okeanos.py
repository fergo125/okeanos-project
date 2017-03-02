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

class  Okeanos(object):
    """docstring for  Okeanos."""
    def __init__(self, params, dataset):
        self.params = params
        self.dataset = dataset

        self.dataset_vars = list()
        self.latitude_array = self.dataset[params.template.variables.lat["var_file_name"]]
        self.longitude_array = self.dataset[params.template.variables.lon["var_file_name"]]

        self.template_dimensions=list()

    def launch(self):
        if self.params.template['type'] == "gif":
            self.create_gif()

    def validate(self):
        self.template_dimensions.append(int(self.params.template.layers["max_lat"]))
        self.template_dimensions.append(int(self.params.template.layers["max_lon"]))
        self.template_dimensions.append(int(self.params.template.layers["min_lat"]))
        self.template_dimensions.append(int(self.params.template.layers["min_lon"]))

        if (self.template_dimensions[0] <= self.latitude_array[len(self.latitude_array)-1] and \
            self.template_dimensions[1] <= self.longitude_array[len(self.longitude_array)-1] and \
            self.template_dimensions[2] >= self.latitude_array[0] and \
            self.template_dimensions[3] >= self.longitude_array[0]) is False:
            print("Bad template dimensions")
            return False

        for var in self.params.template.variables.var:
            if var['var_file_name'] in self.dataset.variables:
                self.dataset_vars.append(self.dataset[var['var_file_name']])
            else:
                print('Var not found in dataset: ',var['var_file_name'])
                return False
        return True

    def create_gif(self):
        pass
            #for layer in params.template.layers.layer:

def main():
    xml= open(sys.argv[1],"r").read()
    print("Params readed")
    params = untangle.parse(xml)
    print("Cargando Archivo:", params.template.datasource.cdata)
    dataset = netCDF4.Dataset(params.template.datasource.cdata,"r")
    print("dataset readed")

    okeanos = Okeanos(params,dataset)

    if okeanos.validate():
        okeanos.launch()
    else:
        print("Error processing parameters")

if __name__=="__main__":
    main()
