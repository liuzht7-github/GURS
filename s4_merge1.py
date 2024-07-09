# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import os
import time
from glob import glob
from multiprocessing import Pool

usecols = ['Id', 'Area', 'ntl_mean', 'geometry']
indir = r"F:\Urban_Rural\dataset\2005\GHS_BUILT_S_TOTAL_2005_Global_step3"
files = glob(indir + r"\\*.shp")

def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd

def merge_sdg(df, outfile):
    tile_ids = list(df['tile_id'].unique())
    tile_ids = [str(x) for x in tile_ids]
    files2 = [file for file in files if os.path.basename(file).split(".")[0].split("_")[-2] + "_" + os.path.basename(file).split(".")[0].split("_")[-1] in tile_ids]
    
    print(len(files2), len(tile_ids))

    tables = [gpd.read_file(file) for file in files2]
    print([file + " reading..." for file in files2])
    
    merged_df = pd.concat(tables, axis=0, ignore_index=True)
    merged_df = merged_df[usecols]
    merged_df = gpd.GeoDataFrame(merged_df)
    merged_df.to_file(outfile, encoding='utf-8')
    return None

if __name__ == '__main__':
    outdir = create_dir(indir.replace("_step3", "_step4"))

    pool = Pool(processes=9)
    start_time = time.time()
    
    ghsl_code = gpd.read_file(r"F:\Urban_Rural\dataset\boundary\GHSL_CODES.shp", encoding='utf-8')
    CCodes = list(ghsl_code['CCode'].unique())
    
    for ccode in CCodes:
        print(ccode, 'Start...')
        df = ghsl_code[ghsl_code['CCode'] == ccode]
        outfile = os.path.join(outdir, f"BUILT_PATCH-v0-{ccode}.shp")
        pool.apply_async(merge_sdg, args=(df, outfile))

    pool.close()
    pool.join()
    
    print('All subprocesses done.')

    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
