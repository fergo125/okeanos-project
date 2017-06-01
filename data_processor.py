import netCDF4 as nc
import numpy as np
import os

#Agregar cada una de las variables para despues procesarlas.
#revisar el nivel del cual se quieren substraer los datos.
#Generar los vectores extra que sean necesarios para animacion.



class DataProcessor(Object):
    #Recibe un pathname creado con os.path.abspath
    def __init__(self, dataset_name):
        file_path = os.path.abspath(dataset_name)
        self.dataset = nc.Dataset(file_path, 'r')
        self.raw_variables = dict()
        self.data_output = dict()

    def process_raw_data(self, variables_names):
        for var in variables_names:
            if len(dataset[var[0]].shape) > 3:
                self.raw_variables[var[0]] = self.dataset[var[0]][var[1]]
            else:
                self.raw_variables[var[0]] = self.dataset[var[0]]

    def process_template_data(self, variables_names):
        for v,d in variables_names:
            self.add_var(v,d['var_type'],d['component_u'],d['component_v'],d['angle'],d['convention'])

    def add_var(self,var_name,var_type='normal',componet_u=None, component_v=None,angle=None, convention="ATM"):
        if var_type == 'normal':
            self.data_output[var_name] = self.raw_variables[var_name]
        if var_type == 'magnitude':
            self.add_magnitude_var(self.dataset,var_name,componet_u, component_v)
        if var_type == 'vector':
            self.add_vector_var(self.dataset,var_name,componet_u, component_v,angle,convention)

    def add_magnitude_var(self,var_name,component_u,component_v):
        data_shape = raw_data[component_u].shape
        self.raw_data[var_name] = np.empty(data_shape)
        for i in range(0,len(self.raw_data.[var_name])):
            self.data_output[var_name][i] = self.calculate_magnitude(raw_data[component_u][i],raw_data[component_v][i])

    def add_vector_var(self,var_name,component_u=None,component_v=None,angle_name=None,convention =None):
        data_shape = raw_data[var_name].shape
        data_output = np.empty((2,data_shape[0],data_shape[1],data_shape[2]))
        for i in range(0,len(self.raw_data[var_name])):
            angle = None
            magnitude = None
            u = self.raw_data[var_name][i]
            v = self.raw_data[var_name][i]
            if component_u is None and component_v is None:
                angle = self.raw_data[angle_name][i]
                magnitude = self.raw_data[var_name][i]
            else:
                angle = np.arctan(u/v)
                magnitude = calculate_magnitude(u,v)
            if convention is "AT":
                data_output[var_name][0][i] = calculate_vector_sin(magnitude,angle)
                data_output[var_name][1][i] = calculate_vector_cos(magnitude,angle)
            if convention is "OC":
                data_output[var_name][0][i] = calculate_vector_cos(magnitude,angle)
                data_output[var_name][1][i] = calculate_vector_sin(magnitude,angle)

    def calculate_vars(self):


    def calculate_magnitude(self,component_u,component_v):
        return np.sqrt(np.power(component_u,2) + np.power(component_v,2))
    def calculate_vector_sin(self,magnitude,direction):
        return magnitude*np.sin(direction)
    def calculate_vector_cos(self,magnitude,direction):
        return magnitude*np.sin(direction)
    def calculate angle(self,d):
        return np.arctan()
