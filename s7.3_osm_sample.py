# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from glob import glob
import os
import time

def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd

year = 2005
indir = f"F:/Urban_Rural/dataset/{year}/GHS_BUILT_S_TOTAL_{year}_Global_step7/merge"
outdir = create_dir(fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step7\osm_sample")
nsample = pd.read_excel(fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step7\osm_con_sample.xlsx")
nsample.set_index('code', inplace=True)
df81_area = pd.read_csv(os.path.join(indir, "merge_area_81.csv"))
df83_area = pd.read_csv(os.path.join(indir, "merge_area_83.csv"))
df81_ntl = pd.read_csv(os.path.join(indir, "merge_ntl_81.csv"))
df83_ntl = pd.read_csv(os.path.join(indir, "merge_ntl_83.csv"))

start_time = time.time()
for i in range(1, 101):
    tables = []
    
    for ccode, table in df81_area.groupby("code"):
        sample_n = nsample.at[int(ccode), 'n81']
        table_samples = table.sample(n=sample_n, ignore_index=False)
        tables.append(table_samples)
    pd.concat(tables, axis=0).to_csv(os.path.join(outdir, f"{i}_sample_area_81.csv"), index=False)
    
    tables = []
    for ccode, table in df83_area.groupby("code"):
        sample_n = nsample.at[int(ccode), 'n83']
        table_samples = table.sample(n=sample_n, ignore_index=False)
        tables.append(table_samples)
    pd.concat(tables, axis=0).to_csv(os.path.join(outdir, f"{i}_sample_area_83.csv"), index=False)
    
    tables = []
    for ccode, table in df81_ntl.groupby("code"):
        sample_n = nsample.at[int(ccode), 'n81']
        table_samples = table.sample(n=sample_n, ignore_index=False)
        tables.append(table_samples)
    pd.concat(tables, axis=0).to_csv(os.path.join(outdir, f"{i}_sample_ntl_81.csv"), index=False)
    
    tables = []
    for ccode, table in df83_ntl.groupby("code"):
        sample_n = nsample.at[int(ccode), 'n83']
        table_samples = table.sample(n=sample_n, ignore_index=False)
        tables.append(table_samples)
    pd.concat(tables, axis=0).to_csv(os.path.join(outdir, f"{i}_sample_ntl_83.csv"), index=False)
    
    print(f"{i} done")

seconds = time.time() - start_time
print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
