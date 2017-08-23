''''sdfsdf'''
import os
import requests as r
import json

API_HOST_ENPOINT_DIR = 'example'
IMAGES_SOURCE_DIRECTORY = 'example'
REGIONS_FILE = 'regions.json'
#format var_names = {'folder_name':'area_id'}

''''sdfsdf'''
def main():
    regions = os.path.abspath(REGIONS_FILE)
    regions_data = json.loads(file(regions,'wb').read())
    images_path = os.path.abspath(IMAGES_SOURCE_DIRECTORY)
    for region in regions_data:
        (dirpath, dirnames, filenames) = os.walk(region['directory'])
        for f in filenames:
            os.remove(os.path.join(dirpath,f))
