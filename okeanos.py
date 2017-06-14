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
from layers import layer_contour,layer_colormesh,layer_title,layer_arrows
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
        variables_dataset = self.process_dataset_variables_parameters()
        self.data_processor.process_dataset_variables(self.process_dataset_variables_parameters())
        variables_template = self.process_template_variables_parameters()
        self.data_processor.process_template_variables(self.process_template_variables_parameters())
        self.data_processor.add_dimensions_variables(self.params.template.variables_dataset.lat.cdata,self.params.template.variables_dataset.lon.cdata,self.params.template.variables_dataset.time.cdata)
        return self.data_processor.validate_dimensions(self.template_dimensions)


    def process_dataset_variables_parameters(self):
        variables_dataset = list()
        for var in self.params.template.variables_dataset.var:
            dataset_var = dict()
            dataset_var["entry_name"] = var.cdata
            dataset_var["output_name"] = var["output_name"]
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
            dataset_var["type"] = var["type"]
            dataset_var["angle"] = var["angle"]
            dataset_var["convention"] = var["convention"]
            variables_template.append(dataset_var)
        return variables_template

#Delete this method.
    def validate(self):
        print('Validating data')
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
             if var['type'] == 'normal' and var.cdata not in self.dataset.variables:
                 print('Var not found in dataset: ',var.cdata)
                 return False
             else:
                if var['type'] == 'normal':
                    self.add_normal_var(self.dataset,var.cdata,level)
                if var['type'] == 'magnitude':
                    self.add_magnitude_var(self.dataset,var.cdata,var['value_u'],var['value_v'],var['level'])
                if var['type'] == 'vector':
                    self.add_vector_var(self.dataset,var.cdata,var['value_u'],var['value_v'],var['level'])
                else:
                    print('Variable type not found')
                    return False
        return True


    def create_collection(self):
        print("Creating with the lon vars: ", self.template_dimensions)
        map_plotter = MapCreator(*self.data_processor.template_dimensions,precision=self.data_processor.data_precision_factor)
        map_plotter.calculate_sub_area(self.data_processor.data_output["lon"],\
                                       self.data_processor.data_output["lat"],\
                                       self.data_processor.data_precision_factor)
        print(self.params.template.layers.layer)
        map_plotter.add_title(self.params.template.title.cdata,self.params.template.title)
        for layer in self.params.template.layers.layer:
            print('Creating layer type:',layer['type'])
            map_plotter.add_layer(layer['type'],layer['var_name'],layer.params)
        collection_name = self.params.template.output.cdata
        if not os.path.exists(collection_name):
            os.makedirs(collection_name)
        map_plotter.create_collection(self.data_processor.data_output,collection_name)

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
