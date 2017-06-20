import netCDF4 as nc
import numpy as np
import os
import scipy as sp
from scipy import interpolate
from mpl_toolkits.basemap import interp

class DataProcessor(object):
    #Recibe un pathname creado con os.path.abspath
    def __init__(self, dataset_name):
        file_path = os.path.abspath(dataset_name)
        self.dataset = nc.Dataset(file_path, 'r')
        self.raw_variables = dict()
        self.data_output = dict()
        self.template_dimensions = list()
        self.sub_indexes = list()
        self.data_precision_factor = None
        self.data_interpolation_factor =None
        self.sub_indexes = list()

    def process_dataset_variables(self, variables_names):
        output_coordenates_x, output_coordenates_y = np.meshgrid(self.data_output["lat"],self.data_output["lon"])
        for var in variables_names:
            process_level = True if len(self.dataset[var["entry_name"]].shape) > 3 else False
            data_shape = self.dataset[var["entry_name"]].shape
            self.raw_variables[var["output_name"]] = np.empty((data_shape[0],len(self.data_output["lat"]),len(self.data_output["lon"])))
            for i in range(0,len(self.dataset[var["entry_name"]])):
                if process_level:
                    interp_fun = self.interpolate_data(np.ma.getdata(self.dataset[var["entry_name"]][i][var["level"]]))
                else:
                    interp_fun = self.interpolate_data(np.ma.getdata(self.dataset[var["entry_name"]][i]))
                self.raw_variables[var["output_name"]][i] = interp_fun


    def process_template_variables(self, variables_names):
        for v in variables_names:
            self.add_var(v['name'],v['type'],v['value_u'],v['value_v'],v['angle'],v['convention'])

    def add_dimensions_variables(self,lat_name,lon_name,time_name):
        self.raw_variables["lat"] = np.sort(self.dataset[lat_name][:])
        self.raw_variables["lon"] = np.sort(self.dataset[lon_name][:])
        self.data_output['time'] = self.raw_variables['time'] = self.dataset[time_name][:]
        self.data_precision_factor = abs(self.raw_variables["lat"][0]-self.raw_variables["lat"][1])


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

    def add_vector_var(self,var_name,component_u=None,component_v=None,angle_name=None,convention ="AT"):
        data_shape = self.raw_variables[component_u].shape
        self.data_output[var_name] = np.empty((data_shape[0],2,data_shape[1],data_shape[2]))
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
                self.data_output[var_name][i][0] = calculate_vector_sin(magnitude,angle)
                self.data_output[var_name][i][1] = calculate_vector_cos(magnitude,angle)
            if convention is "OC":
                self.data_output[var_name][i][0] = calculate_vector_cos(magnitude,angle)
                self.data_output[var_name][i][1] = calculate_vector_sin(magnitude,angle)


    def add_template_dimensions(self,template_dimensions,interpolation_factor=3):
        print('Validating area')
        if (template_dimensions[0] <= self.raw_variables['lat'][len(self.raw_variables['lat'])-1] and \
            template_dimensions[1] <= self.raw_variables['lon'][len(self.raw_variables['lon'])-1] and \
            template_dimensions[2] >= self.raw_variables['lat'][0] and \
            template_dimensions[3] >= self.raw_variables['lon'][0]) is False:
            print("Bad template dimensions")
            return False

        self.data_interpolation_factor = interpolation_factor

        self.template_dimensions = template_dimensions[:]

        lat_vector = np.arange(template_dimensions[2],template_dimensions[0],self.data_precision_factor)
        lon_vector = np.arange(template_dimensions[3],template_dimensions[1],self.data_precision_factor)

        self.calculate_sub_area(lon_vector,lat_vector,self.data_precision_factor)

        self.raw_variables["lat"] = self.raw_variables["lat"][self.sub_indexes[2]:self.sub_indexes[0]]
        self.raw_variables["lon"] = self.raw_variables["lon"][self.sub_indexes[3]:self.sub_indexes[1]]

        print("New latitude vector", self.raw_variables["lat"])
        print("Interporling latitude")
        print("Base Lat:",self.raw_variables["lat"].min()," Max Lat:",self.raw_variables["lat"].max()," New size:", self.raw_variables["lat"].shape[0]*interpolation_factor)

        self.data_output['lat'] = np.linspace(self.raw_variables["lat"].min(),self.raw_variables["lat"].max(),self.raw_variables["lat"].shape[0]*self.data_interpolation_factor)
        self.data_output['lon'] = np.linspace(self.raw_variables["lon"].min(),self.raw_variables["lon"].max(),self.raw_variables["lon"].shape[0]*self.data_interpolation_factor)

        return True

    def calculate_sub_area(self,lon_vector, lat_vector,precision):
        base_lat = self.raw_variables["lat"].min()
        base_lon = self.raw_variables["lon"].min()

        #print('Base_lat: ', base_lat)
        #print('Base_lon: ', base_lon)
        #print('Template max lat: ', lat_vector.max())
        #print('Template max lon: ', lon_vector.max())

        self.sub_indexes.append(int(abs(lat_vector.max()-base_lat)/precision))
        self.sub_indexes.append(int(abs(lon_vector.max()-base_lon)/precision))
        self.sub_indexes.append(int(abs(lat_vector.min()-base_lat)/precision))
        self.sub_indexes.append(int(abs(lon_vector.min()-base_lon)/precision))
        print("Sub Indexes: ", self.sub_indexes)

    def interpolate_data(self,data):
        data_process = data[self.sub_indexes[2]:self.sub_indexes[0]:,self.sub_indexes[3]:self.sub_indexes[1]:]
        #print("lat_data: ", self.raw_variables["lat"])
        #print("lon_data: ", self.raw_variables["lon"])
        #print("lat_interp: ", self.data_output["lat"])
        #print("lon_interp: ", self.data_output["lon"])

        coordinates_xo,coordinates_yo = np.meshgrid(self.data_output["lon"],self.data_output['lat'])

        data_interp = interp(data_process,self.raw_variables["lon"],self.raw_variables['lat'],coordinates_xo,coordinates_yo,masked=False,order=1)
        return data_interp

    def calculate_magnitude(self,component_u,component_v):
        return np.sqrt(np.power(component_u,2) + np.power(component_v,2))
    def calculate_vector_sin(self,magnitude,direction):
        return magnitude*np.sin(direction)
    def calculate_vector_cos(self,magnitude,direction):
        return magnitude*np.sin(direction)
    def calculate_angle(self,d):
        return np.arctan()
