# -*- coding: utf-8 -*-

import arcpy
import os
from glob import glob
from arcpy.sa import *
import time

def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd

if __name__ == "__main__":
    start_time = time.time()

    arcpy.env.overwriteOutput = True
    arcpy.env.parallelProcessingFactor = "0"
    arcpy.env.compression = "LZW"

    indir0 = r"F:\Urban_Rural\dataset\2005\GHS_BUILT_S_TOTAL_2005_Global"
    indir = indir0 + "_step1"
    arcpy.env.workspace = indir

    outdir = create_dir(indir.replace('_step1', '_step2'))
    infiles = glob(indir + r"\*.tif")

    for in_raster in infiles:
        filename = os.path.basename(in_raster)
        out_shp = os.path.join(outdir, filename.replace(".tif", ".shp"))
        
        arcpy.RasterToPolygon_conversion(in_raster, out_shp, "NO_SIMPLIFY", "VALUE")
        print(filename)

    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
