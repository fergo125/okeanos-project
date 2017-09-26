import netCDF4 as nc
import numpy as np
import os
from mpl_toolkits.basemap import interp

class DataProcessor(object):
	#Recibe un pathname creado con os.path.abspath
	def __init__(self, dataset_name, dataset_type):
		if dataset_type == "single":
			file_path = os.path.abspath(dataset_name)
			self.dataset = nc.Dataset(file_path, 'r')
		if dataset_type == "multiple":
			file_path = os.path.abspath(dataset_name)
			self.dataset = nc.MFDataset(file_path, 'r')
		self.raw_variables = dict()
		self.data_output = dict()
		self.template_dimensions = list()
		self.sub_indexes = dict()
		self.data_precision_factor = None
		self.data_interpolation_factor =None
		self.lat_invert = False
		self.lon_inver = False
		self.lon_size = None
		self.lat_size = None


	def process_dataset_area(self, variables_names, reverse_data = True):
		output_coordenates_x, output_coordenates_y = np.meshgrid(self.data_output["lat"],self.data_output["lon"])
		for var in variables_names:
			process_level = True if len(self.dataset[var["entry_name"]].shape) > 3 else False
			data_shape = self.dataset[var["entry_name"]].shape
			self.raw_variables[var["output_name"]] = np.ma.empty((data_shape[0],len(self.data_output["lat"]),len(self.data_output["lon"])))
			#self.raw_variables[var["output_name"]] = np.empty((len(self.data_output["lat"]),len(self.data_output["lon"])))
			for i in range(0,len(self.dataset[var["entry_name"]])):
				var_data = self.dataset[var["entry_name"]][i][var["level"]] if process_level else self.dataset[var["entry_name"]][i]
				interp_data = self.interpolate_data(var_data)
				self.raw_variables[var["output_name"]][i] =  interp_data[::-1] if reverse_data else interp_data


	def process_template_variables(self, variables_names):
		self.data_precision_factor = self.data_precision_factor/self.data_interpolation_factor
		for v in variables_names:
			self.add_var(v['name'],v['type'],v['magnitude'],v['value_u'],v['value_v'],v['angle'])

	def add_dimensions_variables(self,lat_name,lon_name,time_name):
		self.raw_variables["lat"] = self.dataset[lat_name][:]
		self.raw_variables["lon"] = self.dataset[lon_name][:]
		self.raw_variables['time'] = self.dataset[time_name]
		self.data_output['time'] = nc.num2date(self.raw_variables['time'][:],self.raw_variables['time'].units,self.raw_variables['time'].calendar)
		self.data_precision_factor = abs(self.raw_variables["lat"][0]-self.raw_variables["lat"][1])

	def add_var(self,var_name,var_type='normal',magnitude=None,component_u=None, component_v=None,angle=None, convention="AT"):
		if var_type == 'normal':
			self.data_output[var_name] = self.raw_variables[var_name]
		if var_type == 'magnitude':
			self.add_magnitude_var(var_name,component_u, component_v)
		if var_type == 'vector':
			self.add_vector_var(var_name,magnitude,component_u, component_v,angle,convention)

	def add_magnitude_var(self,var_name,component_u,component_v):
		data_shape = self.raw_variables[component_u].shape
		self.data_output[var_name] = np.empty(data_shape)
		for i in range(0,len(self.data_output[var_name])):
			self.data_output[var_name][i] = self.calculate_magnitude(self.raw_variables[component_u][i],self.raw_variables[component_v][i])

	def add_vector_var(self,var_name,magnitude_name=None,component_u=None,component_v=None,angle_name=None,convention ="AT"):
		data_shape = self.raw_variables[component_u].shape if component_u is not None else self.raw_variables[magnitude_name].shape
		#print("Component Shape: ", data_shape)
		self.data_output[var_name] = np.empty((data_shape[0],2,data_shape[1],data_shape[2]))
		for i in range(0,len(self.data_output[var_name])):
			angle = None
			magnitude = None
			if component_u is None and component_v is None:
				##print("Angle input type", type(self.raw_variables[angle_name][i]))

				angle = 90- (self.raw_variables[angle_name][i] - 180)
				magnitude = self.raw_variables[magnitude_name][i]

				##print("Angle output type", type(angle))
				self.data_output[var_name][i][0] = self.calculate_vector_cos(angle)
				self.data_output[var_name][i][1] = self.calculate_vector_sin(angle)

			else:
				u = self.raw_variables[component_u][i]
				v = self.raw_variables[component_v][i]

				angle = np.arctan2(v,u)

				self.data_output[var_name][i][0] = np.cos(angle)
				self.data_output[var_name][i][1] = np.sin(angle)


			##print("Data result:",self.data_output[var_name][i])

	def add_template_dimensions(self,template_dimensions,interpolation_factor=3):
		#print('Validating area')
		if (template_dimensions['max_lat'] <= self.raw_variables['lat'].max() and \
			template_dimensions['max_lon'] <= self.raw_variables['lon'].max() and \
			template_dimensions['min_lat'] >= self.raw_variables['lat'].min() and \
			template_dimensions['min_lon'] >= self.raw_variables['lon'].min()) is False:
			#print("Bad template dimensions")
			return False

		self.data_interpolation_factor = interpolation_factor

		self.template_dimensions = template_dimensions

		lat_vector = np.arange(template_dimensions['min_lat'],template_dimensions['max_lat']+ self.data_precision_factor,self.data_precision_factor)
		lon_vector = np.arange(template_dimensions['min_lon'],template_dimensions['max_lon']+ self.data_precision_factor,self.data_precision_factor)
		self.lat_size = float(self.raw_variables['lat'].shape[0]) - 1
		self.lon_size = float(self.raw_variables['lon'].shape[0]) - 1
		self.calculate_sub_area(lon_vector,lat_vector,self.data_precision_factor)

		if self.raw_variables['lat'][0] > self.raw_variables['lat'][self.lat_size-1]:
			self.raw_variables["lat"] = self.raw_variables["lat"][self.sub_indexes['max_lat']:self.sub_indexes['min_lat']+1:]
		self.raw_variables["lon"] = self.raw_variables["lon"][self.sub_indexes['min_lon']:self.sub_indexes['max_lon']+1:]

		print("lat vector coordinates sub area", self.raw_variables["lat"].min(), self.raw_variables["lat"].max())
		print("lon vector coordinates sub area", self.raw_variables["lon"].min(), self.raw_variables["lon"].max())
		#print("Interporling latitude")
		#print("Base Lat:",self.raw_variables["lat"].min()," Max Lat:",self.raw_variables["lat"].max()," New size:", self.raw_variables["lat"].shape[0]*interpolation_factor)

		self.data_output['lat'] = np.linspace(self.raw_variables["lat"].min(),self.raw_variables["lat"].max(),self.raw_variables["lat"].shape[0]*self.data_interpolation_factor)
		self.data_output['lon'] = np.linspace(self.raw_variables["lon"].min(),self.raw_variables["lon"].max(),self.raw_variables["lon"].shape[0]*self.data_interpolation_factor)

		return True

	def calculate_sub_area(self,lon_vector, lat_vector,precision):
		base_lat = self.raw_variables["lat"].min()
		base_lon = self.raw_variables["lon"].min()
		print("base_lat",base_lat)
		print("base_lon",base_lon)
		# self.sub_indexes['max_lat'] = int(abs(lat_vector.max()-base_lat)/precision)
		# self.sub_indexes['max_lon'] = int(abs(lon_vector.max()-base_lon)/precision)
		# self.sub_indexes['min_lat'] = int(abs(lat_vector.min()-base_lat)/precision)
		# self.sub_indexes['min_lon'] = int(abs(lon_vector.min()-base_lon)/precision)
		# 
		self.sub_indexes['max_lat'] = self.calculate_sub_index(lat_vector.max(),base_lat,precision) 
		self.sub_indexes['max_lon'] = self.calculate_sub_index(lon_vector.max(),base_lon,precision) 
		self.sub_indexes['min_lat'] = self.calculate_sub_index(lat_vector.min(),base_lat,precision) 
		self.sub_indexes['min_lon'] = self.calculate_sub_index(lon_vector.min(),base_lon,precision)

		
		print("lat/lon sizes ", self.lat_size, self.lon_size)
		print("Sub Indexes: ", self.sub_indexes)
		if self.raw_variables['lat'][0] > self.raw_variables['lat'][self.lat_size-1]:
			self.sub_indexes["max_lat"] = self.lat_size - self.sub_indexes["max_lat"]
			self.sub_indexes["min_lat"] = self.lat_size - self.sub_indexes["min_lat"]
		if self.raw_variables['lon'][0] > self.raw_variables['lon'][self.lon_size-1]:
			self.sub_indexes["max_lon"] = self.lon_size - self.sub_indexes["max_lon"]
			self.sub_indexes["min_lon"] = self.lon_size - self.sub_indexes["min_lon"]
			 
		print("Sub Indexes: ", self.sub_indexes)
	
	def calculate_sub_index(self,point,base,precision):
		return int(abs(point-base)/precision)
		
	def interpolate_data(self,data):
		#data_interp = data_process = data[self.sub_indexes[2]:self.sub_indexes[0]+1:,self.sub_indexes[3]:self.sub_indexes[1]+1:]
		data_interp = data_process = data[self.sub_indexes['min_lat']:self.sub_indexes['max_lat']+1:,self.sub_indexes['min_lon']:self.sub_indexes['max_lon']+1:]
		if self.data_interpolation_factor > 1 :
			coordinates_xo,coordinates_yo = np.meshgrid(self.data_output["lon"],self.data_output['lat'])
			data_interp = interp(data_process,np.sort(self.raw_variables["lon"]),np.sort(self.raw_variables['lat']),coordinates_xo,coordinates_yo, masked=True)
			#print(self.data_precision_factor)
		#print("data interp shape", data_interp.shape)
		return data_interp

	def calculate_magnitude(self,component_u,component_v):
		return np.sqrt(component_u**2 + component_v**2)

	def calculate_vector_sin(self,direction):
		#return magnitude*np.sin(direction*np.pi)
		return np.sin(direction*np.pi/180)

	def calculate_vector_cos(self,direction):
		#return magnitude*np.cos(direction*np.pi)
		return np.cos(direction*np.pi/180)

	def calculate_angle(self,d):
		return np.arctan()
