import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from layers.layer import Layer,layer_switcher
import csv
import os


class MapCreator(object):
	#Cambiar el construcctor para que reciba las medidas del netcdf y ademas las de la plantilla
	#def __init__(self,max_lat, max_lon, min_lat, min_lon,precision=2):
	def __init__(self,lat,lon):
		self.map =Basemap(projection='merc',llcrnrlon=lon.min(), \
		urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
		resolution='h')
		self.layers = list()

		self.coordinates_x,self.coordinates_y = self.map(*np.meshgrid(lon,lat))

		self.default_params = {'cmap':'k','shading':'interp',\
								'position':'bottom',\
								'vmin':None,\
								'vmax':None}


	#calcular los subindices en el constructor
	#hacer que cuando se agregue un nuevo layer se le pase unicamente los datos y los subindices
	def add_layer(self,template_type,var_name,params):
		#print(layer_switcher)
		new_layer = layer_switcher[template_type](var_name,self.coordinates_x,self.coordinates_y)
		new_layer.extra_params(params)
		self.layers.append(new_layer)
		return True

	def add_title(self,title,params):
		new_layer = layer_switcher['title'](title)
		new_layer.extra_params(params)
		self.layers.append(new_layer)

	def set_map_title(self,title,font='Open Sans',size='12'):
		self.title = title
		self.font = font
		self.size = int(size)

	def extra_params():
		pass

	def create_collection(self,var_data,collection_name,dpi_image=200,image_width=1,image_height=1,draw_map=True):
		y_axis_text = {'fontsize':6,'rotation':270}
		x_axis_text = {'fontsize':6}
		#Las coordenadas que se van a usar para crea el mapa y despues generar una visualizacion.
		coordinates_x,coordinates_y =  self.map(*np.meshgrid(var_data["lon"],var_data["lat"]))
		#collection_dict = dict()
		csv_header = ["name","date"]
		collection_csv = file(os.path.join(collection_name, 'collection.csv'),'wb')
		csv_writer = csv.DictWriter(collection_csv,fieldnames=csv_header)
		csv_writer.writeheader()
		for data_index in range(0, len(var_data['time'])):
			plt.figure(figsize=(image_width,image_height),dpi=dpi_image,tight_layout=True)
			self.map.drawcoastlines(linewidth=0.4)
			if draw_map:
				self.map.fillcontinents(color="#B4B4B4")
			self.map.drawcountries(linewidth=0.1)
			self.map.drawmapboundary(fill_color="#B4B4B4",linewidth=0.3)
			self.map.drawmeridians(map(lambda x: float(int(x*100))/100,np.linspace(var_data['lon'].min(),var_data['lon'].max(),5)[1:-1]),labels=[0,0,0,1],fontdict=x_axis_text,color='gray',linewidth=0.5)
			self.map.drawparallels(map(lambda x: float(int(x*100))/100,np.linspace(var_data['lat'].min(),var_data['lat'].max(),5)[1:-1]),labels=[1,0,0,0],fontdict=y_axis_text,color='gray',linewidth=0.5)
			for layer in self.layers:
				if type(layer) is layer_switcher['title']:
					layer.render(plt)
				else:
					render_data = var_data[layer.var_name][data_index][:]
					layer.render(self.map,render_data,plt)
				current_date = var_data['time'][data_index]
				frame_date = current_date.strftime("%d-%m-%Y_%H-%M-%S%Z")
				output_date =current_date.strftime("%Y-%m-%dT%H:%M:%S%Z")
				img_name = frame_date+ '.png'
				save_path = os.path.join(collection_name,img_name)
				# collection_buffer += img_name + ","+ output_date + "\n"
			csv_writer.writerow({"name":img_name,"date":output_date})
			print(save_path)
			plt.tight_layout(pad=0, h_pad=0, w_pad=0, rect=(0, 0, 1, 1))
			plt.savefig(save_path, pad_inches=0, bbox_inches='tight', transparent="True")
			plt.close()
		collection_csv.close()
		# json_file = file(os.path.join(collection_name, 'collection.csv'),'wb')
		# json_file.write(json.dumps(collection_dict))
		# json_file.close()
