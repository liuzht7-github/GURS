# -*-coding:utf-8 -*-


import arcpy
import os
from glob import glob
from arcpy.sa import *
import warnings
import time


warnings.filterwarnings("ignore")
arcpy.CheckOutExtension("Spatial")

arcpy.env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = "0"
arcpy.env.compression = "LZW"

def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd

start_time = time.time()

year = 2005
indir = fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step9"
outdir = create_dir(fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step10")
arcpy.env.workspace = indir
files = glob(indir+r"\*.shp")

ntl_shp = "F:/Urban_Rural/dataset/NTL_post/ntl_revise.shp"

for file in files:
    build_layer = "build_lyr"
    arcpy.MakeFeatureLayer_management(file, build_layer, "reclass > 81")
    arcpy.SelectLayerByLocation_management(build_layer, "HAVE_THEIR_CENTER_IN", ntl_shp, selection_type="NEW_SELECTION")

    build_layer2 = "select81"
    arcpy.MakeFeatureLayer_management(file, build_layer2)
    arcpy.SelectLayerByAttribute_management(build_layer2, "NEW_SELECTION", "reclass = 81")
    arcpy.Near_analysis(build_layer, build_layer2)

    update_ids = []
    with arcpy.da.SearchCursor(build_layer, ["id", "NEAR_DIST"]) as cursor:
        for row in cursor:
            if (row[1] <= 1000) & (row[1] >= 0):  
                update_ids.append(row[0])

    arcpy.SelectLayerByAttribute_management(build_layer2, "CLEAR_SELECTION")
    with arcpy.da.UpdateCursor("select81", ["id", "reclass"]) as cursor:
        for row in cursor:
            if row[0] in update_ids:
                row[1] = 81  
                cursor.updateRow(row)

    build_updated_path = os.path.join(outdir, os.path.basename(file))
    arcpy.CopyFeatures_management("select81", build_updated_path)

    print(f"Processed and updated: {build_updated_path}")

    arcpy.Delete_management(build_layer)
        
seconds = time.time() - start_time
print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))

        


