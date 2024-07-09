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
indir = fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step7"
outdir = create_dir(fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step7\merge")

start_time = time.time()

files = glob(indir + r"\*.csv")
areas, ntl_means = [], []

for file in files:
    filename = os.path.basename(file).split(".")[0]
    
    df = pd.read_csv(file)
    df['Area'] = df['Area'] / 1000000
    df['ln_area'] = df['Area'].apply(lambda x: np.log(x + 1))
    df['ln_ntl'] = df['ntl_mean'].apply(lambda x: np.log(x + 1))
    code = filename.split("-")[-1].split("_")[0]
    
    for BuiltType, table in df.groupby('BuiltType'):
        BuiltType = str(int(BuiltType))
        table_ntl = table[['BuiltType', 'ntl_mean', 'ln_ntl']].sort_values(by='ln_ntl', ascending=True)
        table_area = table[['BuiltType', 'Area', 'ln_area']].sort_values(by='ln_area', ascending=True)
        
        table_ntl = table_ntl.iloc[int(len(table_ntl) * 0.005):int(len(table_ntl) * 0.995)]
        table_area = table_area.iloc[int(len(table_area) * 0.005):int(len(table_area) * 0.995)]

        table_ntl['code'] = code
        table_area['code'] = code
        areas.append(table_area)
        ntl_means.append(table_ntl)
    
    print(filename, "done!")

table_area = pd.concat(areas, axis=0, ignore_index=True)
table_ntl = pd.concat(ntl_means, axis=0, ignore_index=True)

for bt, table in table_area.groupby("BuiltType"):
    bt = str(int(bt))
    table.to_csv(outdir + f"\\merge_area_{bt}.csv", index=False)

for bt, table in table_ntl.groupby('BuiltType'):
    bt = str(int(bt))
    table.to_csv(outdir + f"\\merge_ntl_{bt}.csv", index=False)

seconds = time.time() - start_time
print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
