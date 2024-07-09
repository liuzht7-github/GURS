# -*-coding:utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, time
from glob import glob
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
from multiprocessing import cpu_count
from multiprocessing import Pool


def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd


def reclass(area, area_t, ntl, ntl_t):
    if (area > area_t)&(ntl > ntl_t):
        return 81
    if (area > area_t)&(ntl <= ntl_t):
        return 82
    if (area <= area_t)&(ntl <= ntl_t):
        return 83
    if (area <= area_t)&(ntl > ntl_t):
        return 84
    else:
        return 0


year = 2005
outdir = fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step8"


def multiprocess(args):
    file,area,ntl = args
    df = gpd.read_file(file, encoding = 'utf-8')

    df['reclass'] = df.apply(lambda row: reclass(row['Area'], area, row['ntl_mean'],ntl), axis=1)
    df['reclass'] = df['reclass'].astype(dtype=np.int32)

    df.to_file(outdir+r"\\"+os.path.basename(file), encoding = 'utf-8')
    print(file, "done!")
    return None


if __name__ == "__main__":
    start_time = time.time()
    pool = Pool(9)
    indir = fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step7"
    outdir = create_dir(indir.replace("_step7","_step8"))
    files = glob(indir+r"\\*.shp")
    areas = [1.083]*9 
    ntls = [1.948]*9
    values = [files,areas,ntls]
    multiprocess(values)


    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))

