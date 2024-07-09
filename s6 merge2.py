# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import os
import time
from glob import glob
from multiprocessing import Pool

def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd

def merge_patch(indir, Code, outdir):
    files = glob(os.path.join(indir, f"{Code}-*.shp"))
    if files:
        tables = [gpd.read_file(file) for file in files]
        df = pd.concat(tables, axis=0, ignore_index=True)
        df = gpd.GeoDataFrame(df, geometry='geometry').drop(columns=['Id'])
        df['id'] = df.index
        df.to_file(os.path.join(outdir, f"BUILT_PATCH-v0-{Code}.shp"), encoding='utf-8')
    print(Code, "merge done!")

if __name__ == '__main__':
    n_processes = 9
    start_time = time.time()
    
    indir = r"F:\Urban_Rural\dataset\2005\GHS_BUILT_S_TOTAL_2005_Global_step5"
    outdir = create_dir(indir.replace("_step5", "_step6"))

    with Pool(processes=n_processes) as pool:
        for i in range(11):
            pool.apply_async(merge_patch, args=(indir, i, outdir))
        pool.close()
        pool.join()

    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
