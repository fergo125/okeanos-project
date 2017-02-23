import untangle
import netCDF4
from netCDF4 import num2date, date2num
import time
import datetime
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
import os
import sys
import map_creator

params = None
dataset = None

def main():
    xml= open(sys.argv[1],"r").read()
    params = untangle.parse(xml)
    dataset = netCDF4.dataset(params.template.file,"r")

    if params['type'] == "gif":
        create_gif()

if __name__=="main":
    main()

def create_gif():
    dataset_vars = list()
    for var in params.template.variables:
        dataset_vars.append(dataset[])
