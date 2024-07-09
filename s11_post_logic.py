# -*- coding: utf-8 -*-

import os
import geopandas as gpd
import pandas as pd
from glob import glob
import multiprocessing
from multiprocessing import Pool
import time
import numpy as np

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def shp2feather(shp_path, outdir):
    gdf = gpd.read_file(shp_path)
    outfile = outdir + '\\' + os.path.basename(shp_path).replace('.shp', '.feather')
    gdf.to_feather(outfile)
    print(shp_path, "done!")
    return None

def feather2shp(feather_path, outdir):
    gdf = gpd.read_feather(feather_path)
    outfile = outdir + '\\' + os.path.basename(feather_path).replace('.feather', '.shp')
    gdf.to_file(outfile)
    print(feather_path, "done!")
    return None

def process_part(file, year, outdir2):
    data = gpd.read_feather(file)
    data_next = gpd.read_feather(file.replace(str(year), str(year+5)).replace(f'Urban_Rural_Result_out', f'Urban_Rural_Result_in'))
    print(f"Processing {file}...{year}")
    data_curt = data[data['reclass'] == 81]
    data_next_8283 = data_next[data_next['reclass'] > 81]
    data_next_p = gpd.GeoDataFrame(data_next_8283, geometry='geometry')
    data_next_p['geometry2'] = data_next_p.representative_point()
    data_next_p = data_next_p.drop(columns=['geometry'])
    data_next_p = data_next_p.rename(columns={"geometry2": "geometry"})
    data_next_p = gpd.GeoDataFrame(data_next_p, geometry='geometry')
    intersected_data = gpd.sjoin(data_next_p, data_curt[['geometry']], how='inner', predicate='within')
    intersected_data = intersected_data.drop(columns=['index_right'])
    intersected_data = intersected_data.drop_duplicates(subset=['id'], keep='first')
    data_next.loc[intersected_data.index, 'reclass'] = 81
    data_next.reset_index().to_feather(outdir2 + "\\" + os.path.basename(file))
    return 0

def main_processing(year, outdir):
    n_cores = 9
    indir = fr"F:\Urban_Rural\Urban_Rural_Result_in\\" + str(year) if year == 2000 else fr"F:\Urban_Rural\Urban_Rural_Result_out\\" + str(year)
    files = glob(indir + "\\*.feather")
    years = [year] * len(files)
    outdirs = [outdir] * len(files)
    paras = [(x, y, z) for x, y, z in zip(files, years, outdirs)]
    with Pool(n_cores) as pool:
        pool.starmap(process_part, paras)

if __name__ == "__main__":
    start_time = time.time()

    for year in range(2020, 2021, 5):
        with Pool(9) as pool:
            indir = fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step10"
            files = glob(indir + "\\*.shp")
            outdir = create_dir(fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step11")
            pool.starmap(shp2feather, zip(files, [outdir] * len(files)))

    outdir = create_dir(fr"F:\Urban_Rural\Urban_Rural_Result_out")
    outdir2 = create_dir(outdir + r'\\2005')
    main_processing(2000, outdir2)
    for year in [2005, 2010, 2015]:
        outdir2 = create_dir(outdir + f'\\{year + 5}')
        main_processing(year, outdir2)

    for year in range(2000, 2021, 5):
        with Pool(9) as pool:
            indir = fr"F:\Urban_Rural\Urban_Rural_Result_out\{year}"
            files = glob(indir + "\\*.feather")
            outdir = create_dir(fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step11")
            pool.starmap(feather2shp, zip(files, [outdir] * len(files)))

    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
