"""Script para la actulizacion de datos """
import os
import requests as r
import json
import okeanos
import csv

API_HOST_ENPOINT_DIR = 'http://localhost:8000/api/regional_forecasts_slides/'
#IMAGES_SOURCE_DIRECTORY = 'example'
REGIONS_FILE = 'regions.csv'
HOSTNAME="localhost/"
#format var_names = {'folder_name':'area_id'}

''''sdfsdf'''
def main():
    slides_updater()

def slides_updater():
    print("Region's file name:", REGIONS_FILE)
    #regions = os.path(REGIONS_FILE)
    # collection_file = file(REGIONS_FILE, 'r').read()
    # regions_data = json.loads(collection_file)
    #images_path = os.path.abspath(IMAGES_SOURCE_DIRECTORY)
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
                    post_images(os.path.join(region["images_source_directory"],f), region["region_id"],region["images_source_directory"])
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
def post_images(images_csv, region_id, region_source_directory):
    images_result = list()
    #print(images_data)
    with open(images_csv) as images_file:
        images_data = csv.DictReader(images_file)

        for image_data in images_data:
            images_result.append({\
            "region_id":region_id,\
            "date":image_data['date'],\
            "url":HOSTNAME +region_source_directory + image_data["name"]\
            })
    print(images_result)
    request_response = r.post(API_HOST_ENPOINT_DIR, json=images_result,headers={"Content-Type":"application/json"})
    print("Server response: ", request_response.text)

if __name__ == "__main__":
    main()
