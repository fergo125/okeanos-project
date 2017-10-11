"""Script para la actulizacion de datos """
import os
import requests as r
import json
import okeanos
import csv
import argparse
import datetime
import sys

#IMAGES_SOURCE_DIRECTORY = 'example'
API_HOST_ENPOINT_DIR= ""
REGIONS_FILE= ""
HOSTNAME= ""
#format var_names = {'folder_name':'area_id'}

''''sdfsdf'''
def main():
# 	global API_HOST_ENPOINT_DIR
# 	global REGIONS_FILE
# 	global HOSTNAME
	parser = argparse.ArgumentParser(description='Update process for images')
	parser.add_argument('-r','--region',  type=str)
	parser.add_argument('-l','--local',  type=str)
	parser.add_argument('-e','--endpoint',  type=str)
	parser.add_argument('-pf','--parameters_file',  type=str)
	parser.add_argument('-fid','--forecat_id',  type=str)
	parser.add_argument('-ims','--images_source',  type=str)
	parser.add_argument('-ld','--local_direction',  type=str)
	parser.add_argument('-c','--csv_images',  type=str)
	args = parser.parse_args()
	try:
		okeanos.okeanos_invoker(args.parameters_file)
	except IndexError as e:
		sys.exit(status=1)
	post_images(args.images_source, args.forecast_id ,args.local_direction,args.csv_images, args.endpoint,args.local_direction)
	sys.exit(status=0)

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
def post_images(collection_dir, forecast_id, region_entrypoint,csv_filename,hostname,api_endpoint_dir):
	images_result = list()
	#print(images_data)
	images_csv = os.path.join(collection_dir,csv_filename)
	parent_dir = os.path.normpath(images_csv)
	time_now = datetime.datetime.now()
	new_dir_name = time_now.strftime("%Y-%m-%d_%I:%M:%S")	
	new_dir_parent = os.path.join(collection_dir,new_dir_name)
	os.makedirs(new_dir_parent)
	print(new_dir_parent)
	with open(images_csv) as images_file:
		images_data = csv.DictReader(images_file)
		for image_data in images_data:
			old_file = os.path.join(collection_dir,image_data["name"])
			new_file = os.path.join(new_dir_parent,image_data["name"])
			#open(new_file,"w").close()
			os.rename(old_file,new_file)
			images_result.append({\
			"forecast_id":forecast_id,\
			"date":image_data['date'],\
			"url":hostname+ '/' +region_entrypoint+new_dir_name +"/" + image_data["name"]\
			})
	print(images_result)
	request_response = r.post(api_endpoint_dir, json=images_result,headers={"Content-Type":"application/json"})
	#print("Server response: ", request_response.text)

if __name__ == "__main__":
	main()
