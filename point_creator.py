import os
import data_processor
import csv
import requests

class PointCreator(object):
	def __init__(self,var_names):
		self.points = list()
		self.var_names = list()
		self.var_names.append("time")
		self.var_names+=var_names
	
	def add_point(self, lat, lon, file_name):
		point_data = dict()
		point_data["lat"] = lat
		point_data["lon"] = lon
		point_data["filename"] = file_name
		self.points.append(point_data)
		
	def create_collection(self,data,collection_name):
		for point in self.points:
			filename = os.path.abspath(collection_name+"/"+point["filename"]+".csv")
			with open(filename,"wb") as points_file:
				csv_writer = csv.DictWriter(points_file,fieldnames=self.var_names)
				csv_writer.writeheader()
				print("filename:",point["filename"])
				print("point lat:", point['lat'])
				print("point lon:", point['lon'])
				#print (len(data["time"]))
				for i in range(0,len(data["time"])-1):
					row = dict()
					#print(data["time"][i])
					for var_name in self.var_names:
						if var_name == 'time':
							row['time'] = data["time"][i]
						else:
							#print(data[var_name][i])
							if point["filename"] == "puntarenas":
								print(data[var_name][i][point['lat']-5:point['lat']+5][point['lon']-5:point['lon']+5])
							row[var_name] = data[var_name][i][point['lat']][point['lon']]
					csv_writer.writerow(row)