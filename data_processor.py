import netCDF4 as nc
import numpy as np
import os

#Agregar cada una de las variables para despues procesarlas.
#revisar el nivel del cual se quieren substraer los datos.
#Generar los vectores extra que sean necesarios para animacion.



class DataProcessor(object):
    #Recibe un pathname creado con os.path.abspath
    def __init__(self, dataset_name):
        file_path = os.path.abspath(dataset_name)
        self.dataset = nc.Dataset(file_path, 'r')
        self.raw_variables = dict()
        self.data_output = dict()
        self.template_dimensions = list()
        self.data_precision_factor = None

    def process_dataset_variables(self, variables_names):
        for var in variables_names:
            if len(self.dataset[var["entry_name"]].shape) > 3:
                data_shape = self.dataset[var["entry_name"]].shape
                self.raw_variables[var["output_name"]] = np.empty((data_shape[0],data_shape[2],data_shape[3]))
                for i in range(0,len(self.dataset[var["entry_name"]])):
                    self.raw_variables[var["output_name"]][i] = self.dataset[var["entry_name"]][i][var["level"]]
            else:
                self.raw_variables[var["output_name"]] = self.dataset[var["entry_name"]]

    def process_template_variables(self, variables_names):
        for v in variables_names:
            self.add_var(v['name'],v['type'],v['value_u'],v['value_v'],v['angle'],v['convention'])

    def add_dimensions_variables(self,lat_name,lon_name,time_name):
        self.raw_variables['lat'] = self.dataset[lat_name][:]
        self.raw_variables['lon'] = self.dataset[lon_name][:]
        self.raw_variables['time'] = self.dataset[time_name][:]

    def add_var(self,var_name,var_type='normal',componet_u=None, component_v=None,angle=None, convention="ATM"):
        if var_type == 'normal':
            self.data_output[var_name] = self.raw_variables[var_name]
        if var_type == 'magnitude':
            self.add_magnitude_var(var_name,componet_u, component_v)
        if var_type == 'vector':
            self.add_vector_var(var_name,componet_u, component_v,angle,convention)

    def add_magnitude_var(self,var_name,component_u,component_v):
        data_shape = self.raw_variables[component_u].shape
        self.data_output[var_name] = np.empty(data_shape)
        for i in range(0,len(self.data_output[var_name])):
            self.data_output[var_name][i] = self.calculate_magnitude(self.raw_variables[component_u][i],self.raw_variables[component_v][i])

    def add_vector_var(self,var_name,component_u=None,component_v=None,angle_name=None,convention =None):
        data_shape = self.raw_variables[component_u].shape
        self.data_output[var_name] = np.empty((2,data_shape[0],data_shape[1],data_shape[2]))
        for i in range(0,len(self.data_output[var_name])):
            angle = None
            magnitude = None
            u = self.raw_variables[component_u][i]
            v = self.raw_variables[component_v][i]
            if component_u is None and component_v is None:
                angle = self.raw_variables[angle_name][i]
                magnitude = self.raw_variables[var_name][i]
            else:
                angle = np.arctan(u/v)
                magnitude = self.calculate_magnitude(u,v)
            if convention is "AT":
                self.data_output[var_name][0][i] = calculate_vector_sin(magnitude,angle)
                self.data_output[var_name][1][i] = calculate_vector_cos(magnitude,angle)
            if convention is "OC":
                self.data_output[var_name][0][i] = calculate_vector_cos(magnitude,angle)
                self.data_output[var_name][1][i] = calculate_vector_sin(magnitude,angle)


    def validate_dimensions(self,template_dimensions):
        print('Validating data')
        if (template_dimensions[0] <= self.raw_variables['lat'][len(self.raw_variables['lat'])-1] and \
            template_dimensions[1] <= self.raw_variables['lon'][len(self.raw_variables['lon'])-1] and \
            template_dimensions[2] >= self.raw_variables['lat'][0] and \
            template_dimensions[3] >= self.raw_variables['lon'][0]) is False:
            print("Bad template dimensions")
            return False
        self.template_dimensions = template_dimensions[:]
        self.data_output['lat'] = self.raw_variables['lat']
        self.data_output['lon'] = self.raw_variables['lon']
        self.data_output['time'] = self.raw_variables['time']
        self.data_precision_factor = abs(self.raw_variables['lon'][0]-self.raw_variables["lon"][1])
        return True


    def calculate_magnitude(self,component_u,component_v):
        return np.sqrt(np.power(component_u,2) + np.power(component_v,2))
    def calculate_vector_sin(self,magnitude,direction):
        return magnitude*np.sin(direction)
    def calculate_vector_cos(self,magnitude,direction):
        return magnitude*np.sin(direction)
    def calculate_angle(self,d):
        return np.arctan()
