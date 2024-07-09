# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
from glob import glob
import rasterio
import time

def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd

if __name__ == "__main__":
    start_time = time.time()

    root = r"F:\Urban_Rural\dataset\2005\\"
    indir = root + "GHS_BUILT_S_TOTAL_2005_Global"
    files = glob(indir + r"\\*.tif")
    outdir = create_dir(indir + r"_step1")
    
    threshold1 = 1000
    for file in files:
        filename = os.path.basename(file)
        with rasterio.open(file) as src_dataset:
            profile = src_dataset.profile
            band1 = src_dataset.read(1)
            
            band1[band1 == profile['nodata']] = 0
            band1[band1 < threshold1] = 0
            new_array1 = band1 >= threshold1

        final_array = new_array1.astype(int) * 80
        final_array = final_array.astype(np.uint16)
        profile.update(nodata=0)
        
        out_file = os.path.join(outdir, filename)
        with rasterio.open(out_file, 'w', **profile) as dst:
            dst.write(final_array, 1)
        print(filename, "done!")

    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
