"""docstring for  Okeanos."""
import os
import sys
import untangle
from map_creator import MapCreator
from point_creator import PointCreator
from layers import layer_contour, layer_colormesh, layer_title, layer_arrows, layer_stream
from data_processor import DataProcessor

reload(sys) # just to be sure
sys.setdefaultencoding('utf-8')

class Okeanos(object):
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

		self.data_processor = DataProcessor(dataset_name, self.params.template.variables_dataset['type'])

		self.reverse_data = False if self.params.template.variables_dataset['reverse'] == "false" else True
		
		#Se agrega las dimensiones del dataset
		self.data_processor.add_dimensions_variables(self.params.template.variables_dataset.lat.cdata,\
													self.params.template.variables_dataset.lon.cdata,\
													self.params.template.variables_dataset.time.cdata,\
													self.reverse_data)
		
		if self.params.template.output["type"] == "images":
			self.template_dimensions = dict()
			self.template_dimensions['max_lat'] = int(self.params.template.layers["max_lat"])
			self.template_dimensions['max_lon'] = int(self.params.template.layers["max_lon"])
			self.template_dimensions['min_lat'] = int(self.params.template.layers["min_lat"])
			self.template_dimensions['min_lon'] = int(self.params.template.layers["min_lon"])
			self.interpolation_factor = int(self.params.template.layers["interpolation_factor"])
		if self.params.template.output["type"] == "csv":
			self.template_dimensions = dict()
			self.template_dimensions['max_lat'] = self.data_processor.raw_variables["lat"].max()
			self.template_dimensions['max_lon'] = self.data_processor.raw_variables["lon"].max()
			self.template_dimensions['min_lat'] = self.data_processor.raw_variables["lat"].min()
			self.template_dimensions['min_lon'] = self.data_processor.raw_variables["lon"].min()
			print(self.template_dimensions)
			self.interpolation_factor =  int(self.params.template.points["interpolation_factor"])
	
#this vectors are no longer necesary
		#self.latitude_array = self.dataset[params.template.variables.lat.cdata][:]
		#self.longitude_array = self.dataset[params.template.variables.lon.cdata][:]

#The data processor is in charge to put the data in the right format for the map creation
		

#this vectors are no longer necesary
		#self.variables_data['time'] = self.dataset[params.template.variables.time.cdata][:]
		#self.template_dimensions=list()
		#self.data_processor = data_processor(dataset_name)

	def launch(self):
		self.create_collection()


#Pasar esto a data_processor
	def process_vars(self):
		#De ser necesario revertir los datos se revierten
	
		if  not self.data_processor.add_template_dimensions(self.template_dimensions,self.interpolation_factor):
			return False
		
		#Se extraen las variables del dataset descritas en la plantilla
		variables_dataset = self.process_dataset_variables_parameters()
		
		#Se extraen y se revierten los datos de las variables del dataset que se van a usar
		self.data_processor.process_dataset_area(variables_dataset,self.reverse_data)
		
		#Se extraen los nombres de las variables como se van a usar en la plantilla
		self.variables_template = self.process_template_variables_parameters()

		#Se procesan las variables como se van a usar en la plantilla
		self.data_processor.process_template_variables(self.variables_template)
			
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
		collection_name = os.path.normpath(self.params.template.output.cdata)
		if not os.path.exists(collection_name):
			os.makedirs(collection_name)
		if self.params.template.output["type"] == "images":
			self.create_images(collection_name)
		if self.params.template.output["type"] == "csv":
			self.create_points(collection_name)
		
		#Para generar una imagen cuadrada se usa una resolucion de 3.2x2.7 despues se cambia para el dpi para lo que sea necesario
		
	def create_images(self,collection_name):
		map_plotter = MapCreator(self.data_processor.data_output["lat"],self.data_processor.data_output["lon"])
		if self.params.template.title.cdata != "":
			map_plotter.add_title(self.params.template.title.cdata,self.params.template.title)
		draw_map = True
		if self.params.template.layers["draw_map"] is not None:
			draw_map = True if self.params.template.layers["draw_map"] == "True" else False
		for layer in self.params.template.layers.layer:
			map_plotter.add_layer(layer['type'],layer['var_name'],layer.params)
		map_plotter.create_collection(self.data_processor.data_output,collection_name,draw_map = draw_map,dpi_image=150,image_width=2.7,image_height=3.2)
	
	def create_points(self,collection_name):
		csv_data_points = list()
		var_names = map(lambda d: d["name"], self.variables_template)
		point_creator = PointCreator(var_names)
		for point in self.params.template.points.point:
			point_csv = dict()
			print(self.template_dimensions["max_lat"],self.template_dimensions["max_lon"])
			lat_index = self.data_processor.calculate_sub_index(float(point['lat']),\
													self.template_dimensions["min_lat"],\
													self.data_processor.data_precision_factor)
			
			lon_index = self.data_processor.calculate_sub_index(float(point['lon']),\
													self.template_dimensions["min_lon"],\
													self.data_processor.data_precision_factor)
			file_name = point.cdata
			point_creator.add_point(lat_index,lon_index,file_name)
		#print(self.data_processor.raw_variables)
		print(self.data_processor.sub_indexes)
		point_creator.create_collection(self.data_processor.data_output,collection_name)
def okeanos_invoker(xmlfilename):
	xml= open(xmlfilename,"r").read()
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


def main():
	okeanos_invoker(sys.argv[1])

if __name__=="__main__":
	main()
