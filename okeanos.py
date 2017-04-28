import untangle
import netCDF4
from netCDF4 import num2date, date2num
import time
import datetime
import numpy as np
import os
#import map_plotter_creator
import sys
#import map_plotter_creator.map_plotterCreator
from map_creator import MapCreator
from layers import layer_contour,layer_colormesh

reload(sys) # just to be sure
sys.setdefaultencoding('utf-8')

class  Okeanos(object):
    """docstring for  Okeanos."""
    def __init__(self, params, dataset):
        self.params = params
        self.dataset = dataset

        self.dataset_vars = list()
        self.latitude_array = self.dataset[params.template.variables.lat["var_file_name"]][:]
        self.longitude_array = self.dataset[params.template.variables.lon["var_file_name"]][:]

        self.template_dimensions=list()
        self.data_precision_factor= abs(self.latitude_array[1]-self.latitude_array[0])

        #testing with the file lat and lon
        #self.template_dimensions.append(self.latitude_array.max())
        #self.template_dimensions.append(self.longitude_array.max())
        #self.template_dimensions.append(self.latitude_array.min())
        #self.template_dimensions.append(self.longitude_array.min())

    def launch(self):
        if self.params.template['type'] == "gif":
            self.create_collection()

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
            if var['var_file_name'] not in self.dataset.variables:
                print('Var not found in dataset: ',var['var_file_name'])
                return False
        return True

    def create_collection(self):
        print("Creating with the lon vars: ", self.template_dimensions)
        map_plotter = MapCreator(*self.template_dimensions,precision=self.data_precision_factor)
        map_plotter.calculate_sub_area(self.longitude_array,self.latitude_array,self.data_precision_factor)
        print(self.params.template.layers.layer)
        for layer in self.params.template.layers.layer:
            print('Creating layer type:',layer['type'])
            map_plotter.add_layer(layer['type'],layer['var_name'])
        collection_name = self.params.template.output.cdata
        if not os.path.exists(collection_name):
            os.makedirs(collection_name)
        map_plotter.create_collection(self.dataset,collection_name)

def main():
    xml= open(sys.argv[1],"r").read()
    print("Params read")
    params = untangle.parse(xml)
    print("Cargando Archivo:", params.template.datasource.cdata)
    dataset = netCDF4.Dataset(params.template.datasource.cdata,"r")
    print("dataset read")
    okeanos = Okeanos(params,dataset)
    if okeanos.validate():
        okeanos.launch()
    else:
        print("Error processing parameters")

if __name__=="__main__":
    main()
