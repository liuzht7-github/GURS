# -*- coding: utf-8 -*-

import geopandas as gpd
import os
import time
from glob import glob
from multiprocessing import Pool

def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd

def split_batch(file, outdir, boundary):
    filename = os.path.basename(file)
    CCode = filename.split(".")[0].split("-")[-1]
    df = gpd.read_file(file)
    df.sindex
    df_sjoin = gpd.sjoin(df, boundary, predicate='within', how='left')
    df_sjoin = df_sjoin.drop(columns=['index_right'])
    df_sjoin.fillna(0, inplace=True)
    for ccode, table in df_sjoin.groupby('CCode'):
        ccode = int(ccode)
        output_filename = f"{ccode}-{CCode}.shp" if ccode != 0 else f"{CCode}-00.shp"
        table.to_file(os.path.join(outdir, output_filename), encoding='utf-8')
    print(file, "split done!")
    return None

if __name__ == '__main__':
    n_processes = 9
    pool = Pool(processes=n_processes)
    start_time = time.time()

    indir = r"F:\Urban_Rural\dataset\2005\GHS_BUILT_S_TOTAL_2005_Global_step4"
    outdir = create_dir(indir.replace("_step4", "_step5"))
    files = glob(indir + r"\\*.shp")
    
    boundary_path = r"F:\Urban_Rural\dataset\boundary"
    boundary = gpd.read_file(os.path.join(boundary_path, "world_class_code.shp"))
    boundary = boundary[['CCode', 'geometry']]
    boundary.sindex
    
    for file in files:
        pool.apply_async(split_batch, args=(file, outdir, boundary))
    pool.close()
    pool.join()

    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
