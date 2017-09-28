"""Script para la actulizacion de datos """
import os
import requests as r
import json
import okeanos
import csv
import argparse
import datetime

#IMAGES_SOURCE_DIRECTORY = 'example'
API_HOST_ENPOINT_DIR= ""
REGIONS_FILE= ""
HOSTNAME= ""
#format var_names = {'folder_name':'area_id'}

''''sdfsdf'''
def main():
	global API_HOST_ENPOINT_DIR
	global REGIONS_FILE
	global HOSTNAME
	parser = argparse.ArgumentParser(description='Update process for images')
	parser.add_argument('-r','--region',  type=str)
	parser.add_argument('-l','--local',  type=str)
	parser.add_argument('-e','--endpoint',  type=str)
	args = parser.parse_args()
	API_HOST_ENPOINT_DIR = args.endpoint
	REGIONS_FILE = args.region
	HOSTNAME = args.local
	print(API_HOST_ENPOINT_DIR,REGIONS_FILE,HOSTNAME)
	slides_updater()

def slides_updater():
	print("Region's file name:", REGIONS_FILE)
	with open(REGIONS_FILE,'r') as regions_file:
		regions_data = csv.DictReader(regions_file)
		print(regions_data)
		for region in regions_data:
			print(region)
			if os.path.exists(os.path.normpath(region['images_source_directory'])):
				delete_old_files(region['images_source_directory'])
			okeanos.okeanos_invoker(region['parameters_file'])
			for f in os.listdir(region["images_source_directory"]):
				if f.endswith(".csv"):
					post_images(os.path.join(region["images_source_directory"],f), region["forecast_id"],region["local_direction"])
def delete_old_files(directory):
	print(os.path.abspath(directory))
	walker = os.walk(os.path.abspath(directory))
	for dirpath, dirname, filenames in walker:
		print(dirpath)
		print(filenames)
		for filename in filenames:
			os.remove(os.path.join(dirpath, filename))
	# if len(filenames) > 0:
	#          os.remove(os.path.join(dirpath, filename))
	#      for filename in filenames:
def post_images(images_csv, forecast_id, region_entrypoint):
	images_result = list()
	#print(images_data)
	parent_dir = os.path.basename(images_csv)
	time_now = datetime.datetime.now()
	new_dir_name = time_now.strftime("%Y-%m-%d_%I:%M:%S")	
	new_dir_parent = os.path.join(parent_dir,new_dir_name)
	os.makedirs(new_dir_parent)
	with open(images_csv) as images_file:
		images_data = csv.DictReader(images_file)
		for image_data in images_data:		
			os.rename(parent_dir+images_csv,new_dir_parent+images_csv)
			images_result.append({\
			"forecast_id":forecast_id,\
			"date":image_data['date'],\
			"url":HOSTNAME+ '/' +region_entrypoint + image_data["name"]\
			})
	print(images_result)
	request_response = r.post(API_HOST_ENPOINT_DIR, json=images_result,headers={"Content-Type":"application/json"})
	#print("Server response: ", request_response.text)

if __name__ == "__main__":
	main()
