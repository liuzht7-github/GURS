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


year = 2005
outdir = fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step9"


def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd


def multiprocess(file, thresholds=[]):
    df = gpd.read_file(file, encoding='utf-8')
    df_urban = df.loc[df['reclass'] == 81]
    df_island = df.loc[df['reclass'] == 84]
    df_other = df.loc[(df['reclass'] == 82) | (df['reclass'] == 83)]

    df_island_temp = gpd.GeoDataFrame(df_island)
    df_urban_temp = gpd.GeoDataFrame(df_urban)
    df_island_temp['id'] = df_island_temp.index

    for threshold in thresholds:
        df_island_near = gpd.sjoin_nearest(df_island_temp, df_urban_temp[['geometry']], distance_col="near_dis")
        df_island_near = df_island_near.drop(columns=['index_right'])
        df_island_near = df_island_near.drop_duplicates(subset=['id'])

        df_urban2 = df_island_near.loc[df_island_near['near_dis'] <= threshold]
        df_urban2.drop(columns=['near_dis'], inplace=True)
        df_urban_temp = pd.concat([df_urban_temp, df_urban2], axis=0, ignore_index=True)

        df_island_temp = df_island_near.loc[df_island_near['near_dis'] > threshold]
        df_island_temp.drop(columns=['near_dis'], inplace=True)
        df_island_temp['id'] = df_island_temp.index

    df_urban_temp['reclass'] = 81
    df_island_temp['reclass'] = 83

    df = pd.concat([df_other, df_urban_temp, df_island_temp], axis=0, ignore_index=True)
    df.to_file(outdir + r"\\" + os.path.basename(file), encoding='utf-8')

    print(file, "done!")
    return None


if __name__ == "__main__":
    start_time = time.time()
    pool = Pool(9)

    indir = fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step8"
    outdir = create_dir(indir.replace("_step8", "_step9"))
    files = glob(indir + r"\\*.shp")
    multiprocess(files)


    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
