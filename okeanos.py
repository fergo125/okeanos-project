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
from layers import layer_contour,layer_colormesh,layer_title,layer_arrows,layer_stream
from data_processor import DataProcessor

reload(sys) # just to be sure
sys.setdefaultencoding('utf-8')

class  Okeanos(object):
    """docstring for  Okeanos."""
    def __init__(self, params, dataset_name):
        self.params = params
        # self.dataset = dataset
        self.variables_data = dict()

        self.dataset_vars = list()

#List with names and characteristics of the dataset variables
        self.variables_dataset = list()

#List with names and characteristics of the template variables
        self.variables_template = list()

        self.template_dimensions = list()
        self.template_dimensions.append(int(self.params.template.layers["max_lat"]))
        self.template_dimensions.append(int(self.params.template.layers["max_lon"]))
        self.template_dimensions.append(int(self.params.template.layers["min_lat"]))
        self.template_dimensions.append(int(self.params.template.layers["min_lon"]))

        self.interpolation_factor = int(self.params.template.layers["interpolation_factor"])

#this vectors are no longer necesary
        #self.latitude_array = self.dataset[params.template.variables.lat.cdata][:]
        #self.longitude_array = self.dataset[params.template.variables.lon.cdata][:]

#The data processor is in charge to put the data in the right format for the map creation
        self.data_processor =  DataProcessor(dataset_name)

#this vectors are no longer necesary
        #self.variables_data['time'] = self.dataset[params.template.variables.time.cdata][:]
        #self.template_dimensions=list()
        #self.data_processor = data_processor(dataset_name)

    def launch(self):
        if self.params.template.output['type'] == "collection":
            self.create_collection()

#Pasar esto a data_processor
    def process_vars(self):
        self.data_processor.add_dimensions_variables(self.params.template.variables_dataset.lat.cdata,self.params.template.variables_dataset.lon.cdata,self.params.template.variables_dataset.time.cdata)
        if  not self.data_processor.add_template_dimensions(self.template_dimensions,self.interpolation_factor):
            return False
        variables_dataset = self.process_dataset_variables_parameters()
        self.data_processor.process_dataset_variables(self.process_dataset_variables_parameters())
        variables_template = self.process_template_variables_parameters()
        self.data_processor.process_template_variables(self.process_template_variables_parameters())
        return True

    def process_dataset_variables_parameters(self):
        variables_dataset = list()
        for var in self.params.template.variables_dataset.var:
            dataset_var = dict()
            dataset_var["entry_name"] = var.cdata
            dataset_var["output_name"] = var["output_name"]
            if var["level"] is not None:
                dataset_var["level"] = int(var["level"])
            variables_dataset.append(dataset_var)
        return variables_dataset

    def process_template_variables_parameters(self):
        variables_template = list()
        for var in self.params.template.variables_template.var:
            dataset_var = dict()
            dataset_var["name"] = var.cdata
            dataset_var["value_u"] = var["value_u"]
            dataset_var["value_v"] = var["value_v"]
            dataset_var["magnitude"] = var["magnitude"]
            dataset_var["type"] = var["type"]
            dataset_var["angle"] = var["angle"]
            dataset_var["convention"] = var["convention"]
            variables_template.append(dataset_var)
        return variables_template


    def create_collection(self):
        print("Creating with the lon vars: ", self.template_dimensions)
        map_plotter = MapCreator(self.data_processor.data_output["lat"],self.data_processor.data_output["lon"])
        print(self.params.template.layers.layer)
        map_plotter.add_title(self.params.template.title.cdata,self.params.template.title)
        draw_map = True
        if self.params.template.layers["draw_map"] is not None:
            draw_map = True if self.params.template.layers["draw_map"] == "True" else False
        for layer in self.params.template.layers.layer:
            print('Creating layer type:',layer['type'])
            map_plotter.add_layer(layer['type'],layer['var_name'],layer.params)
        collection_name = self.params.template.output.cdata
        if not os.path.exists(collection_name):
            os.makedirs(collection_name)
        map_plotter.create_collection(self.data_processor.data_output,collection_name,200,draw_map)

def main():
    xml= open(sys.argv[1],"r").read()
    print("Params read")
    params = untangle.parse(xml)
    print("Cargando Archivo:", params.template.variables_dataset["datasource"])
    #dataset = netCDF4.Dataset(params.template.datasource.cdata,"r")
    print("dataset read")
    okeanos = Okeanos(params,params.template.variables_dataset["datasource"])
    if okeanos.process_vars():
        okeanos.launch()
    else:
        print("Error processing parameters")

if __name__=="__main__":
    main()
