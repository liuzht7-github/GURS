# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
import time
from glob import glob
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
from multiprocessing import Pool

def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd

NTL_file = r"F:\Urban_Rural\dataset\2005\NTL\NTL_2005_100m.tif"

def zonal_ntl(patch_file, outdir):
    gdf_area = gpd.read_file(patch_file)
    filename = os.path.basename(patch_file)
    
    gdf_area['Area'] = gdf_area.area.astype(np.int32)
    
    gdf_area_4326 = gdf_area.to_crs(epsg=4326)
    stats = zonal_stats(gdf_area_4326, NTL_file, stats=['mean'])
    df_stats = pd.DataFrame(stats).fillna(-10000)
    ntl_values = [(x + 10000) / 100 for x in df_stats['mean']]
    gdf_area_4326['ntl_mean'] = ntl_values.astype(np.float32)
    gdf_area_zonal = gdf_area_4326.to_crs(gdf_area.crs)
    
    gdf_area_zonal.to_file(os.path.join(outdir, filename), encoding='utf-8')
    print(filename, "done!")
    return None

if __name__ == "__main__":
    indir = r"F:\Urban_Rural\dataset\2005\GHS_BUILT_S_TOTAL_2005_Global_step2_1"
    outdir = create_dir(indir.replace("_step2", "_step3"))

    start_time = time.time()
    files = glob(indir + r"\\*.shp")

    print("Starting......")
    with Pool(processes=9) as pool:
        for file in files:
            pool.apply_async(zonal_ntl, args=(file, outdir))
        pool.close()
        pool.join()

    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
