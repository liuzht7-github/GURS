# -*- coding: utf-8 -*-

import pandas as pd
from glob import glob
import geopandas as gpd
from multiprocessing import Pool
import time, os
import numpy as np

def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd

def reclasstype(x):
    if x in ['city']:
        return 'urban'
    elif x in ['town', 'suburb']:
        return 'town'
    elif x in ['village', 'hamlet', 'farm']:
        return 'rural'
    else:
        return 'other'

def recode(urban, town, rural):
    if urban > 0:
        return 81
    elif town > 0:
        return 82
    elif rural > 0:
        return 83
    else:
        return 80

osm_T = 200
def osm_cls(infile, df_osm, outfile):
    df_left = gpd.read_file(infile)
    for fclass in ['urban', 'town', 'rural']:
        df_right = df_osm.loc[df_osm['place2'] == fclass][['osm_id', 'geometry']]
        df_left = gpd.sjoin_nearest(df_left, df_right, max_distance=osm_T, how='left', lsuffix='left', rsuffix='right')
        df_left = df_left.drop_duplicates(subset=['id'], keep='first').drop(columns=['index_right'])
        df_left = df_left.rename(columns={'osm_id': fclass}).fillna(0)
        df_left[fclass] = df_left[fclass].astype(np.int64)
    
    df_left['BuiltType'] = df_left.apply(lambda row: recode(row['urban'], row['town'], row['rural']), axis=1).astype(np.int16)
    df_1 = df_left[['id', 'BuiltType', 'geometry', 'Area', 'ntl_mean']]
    df_1.to_file(outfile, encoding='utf-8')
    
    df_2 = df_1[['id', 'BuiltType', 'Area', 'ntl_mean']]
    df_2.loc[df_2['BuiltType'] == 81].to_csv(outfile.replace(".shp", "_81.csv"), encoding='utf-8', index=False)
    df_2.loc[df_2['BuiltType'] == 83].to_csv(outfile.replace(".shp", "_83.csv"), encoding='utf-8', index=False)
    return None

if __name__ == '__main__':
    pool = Pool(processes=9)
    start_time = time.time()
    year = 2005

    indir = fr"F:\Urban_Rural\dataset\{year}\\"
    path_osm = r"F:\Urban_Rural\dataset\OSM\projected_osm.shp"
    path_merge = os.path.join(indir, f"GHS_BUILT_S_TOTAL_{year}_Global_step6")
    outdir = create_dir(path_merge.replace("_step6", "_step7"))

    df_osm = gpd.read_file(path_osm)
    df_osm['place2'] = df_osm['place'].apply(reclasstype)
    df_osm = df_osm.loc[df_osm['place2'] != 'other']

    files = glob(path_merge + "\\*.shp")
    for file in files:
        print(file, 'Start......')
        outpath = os.path.join(outdir, os.path.basename(file))
        pool.apply_async(osm_cls, args=(file, df_osm, outpath))
        print(file, 'Finish!')

    pool.close()
    pool.join()

    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
