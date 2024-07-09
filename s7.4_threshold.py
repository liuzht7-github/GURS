# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
from glob import glob
import geopandas as gpd
import statsmodels.api as sm

def create_dir(cwd):
    if not os.path.exists(cwd):
        os.makedirs(cwd)
    return cwd

def find_t(x1,x2,y1,y2,interval):
    T = 0
    f1 = interp1d(x1, y1)
    f2 = interp1d(x2, y2)
    minx = max(min(x1),min(x2))
    maxx = min(max(x1),max(x2))
    xnew = np.arange(minx, maxx, interval)

    ynew1 = f1(xnew)
    ynew2 = f2(xnew)
    n = len(xnew)
    for i in range(1,n-1):
        if (ynew1[i-1]-ynew2[i-1])*(ynew1[i+1]-ynew2[i+1])<=0:
            T = xnew[i]
            Y = ynew1[i]
            return round(T,6),Y,xnew,ynew1,ynew2

if __name__ == "__main__":
    start_time = time.time()
    year = 2005
    indir = fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step7\osm_sample"
    outdir = create_dir(fr"F:\Urban_Rural\dataset\{year}\GHS_BUILT_S_TOTAL_{year}_Global_step7\osm_sample\outfile")
    files = glob(indir + "/*.csv")

    tp = 'ntl'
    rows=[]
    for i in range(1,101):
        file81 = indir+"\\"+f'{i}_sample_{tp}_81.csv'
        file83 = indir+"\\"+f'{i}_sample_{tp}_83.csv'
        df81 = pd.read_csv(file81)
        df83 = pd.read_csv(file83)

        ntl1 = df81['ln_ntl']
        ntl2 = df83['ln_ntl']

        intervals1 = list(np.arange(0, np.around(ntl1.max(),1)+0.05, 0.05))
        intervals2 = list(np.arange(0, np.around(ntl2.max(),1)+0.05, 0.05))
        intervals1 = [round(x,2) for x in intervals1]
        intervals2 = [round(x,2) for x in intervals2]

        hist, bin_edges = np.histogram(ntl1, bins=intervals1)
        freq_percentages = hist/len(ntl1)
        cumulative_freq = np.cumsum(freq_percentages)

        hist, bin_edges2 = np.histogram(ntl2, bins=intervals2)
        freq_percentages2 = hist/len(ntl2)
        cumulative_freq2 = np.cumsum(freq_percentages2)

        cumulative_freq2 = [1-x for x in cumulative_freq2]

        x1 = np.delete(intervals1,-1)
        freq1 = cumulative_freq

        freq2 = np.insert(cumulative_freq2,0,1)
        x2 = list(intervals2)

        res1 = pd.DataFrame({'x':x1,'y':freq1})
        res2 = pd.DataFrame({'x':x2,'y':freq2})

        lowess = sm.nonparametric.lowess
        y1 = lowess(res1['y'], res1['x'],frac=0.03)
        y2 = lowess(res2['y'], res2['x'],frac=0.03)

        T,Y,xnew,ynew1,ynew2 = find_t(y1[:,0],y2[:,0],y1[:,1],y2[:,1],interval=0.001)
        ntl = np.exp(T)-1
        rows.append([i,T,Y,ntl])
        print(i)

    df = pd.DataFrame(rows,columns=['id','T','Y','ntl'])
    df.to_csv(outdir+f'\\{tp}_mean.csv',index=False)

    tp = 'area'
    rows=[]
    for i in range(1,101):
        file81 = indir+"\\"+f'{i}_sample_{tp}_81.csv'
        file83 = indir+"\\"+f'{i}_sample_{tp}_83.csv'
        df81 = pd.read_csv(file81)
        df83 = pd.read_csv(file83)

        ntl1 = df81['ln_area']
        ntl2 = df83['ln_area']

        intervals1 = list(np.arange(0, np.around(ntl1.max(),1)+0.03, 0.03))
        intervals2 = list(np.arange(0, np.around(ntl2.max(),1)+0.03, 0.03))
        intervals1 = [round(x,2) for x in intervals1]
        intervals2 = [round(x,2) for x in intervals2]

        hist, bin_edges = np.histogram(ntl1, bins=intervals1)
        freq_percentages = hist/len(ntl1)
        cumulative_freq = np.cumsum(freq_percentages)

        hist, bin_edges2 = np.histogram(ntl2, bins=intervals2)
        freq_percentages2 = hist/len(ntl2)
        cumulative_freq2 = np.cumsum(freq_percentages2)

        cumulative_freq2 = [1-x for x in cumulative_freq2]

        x1 = np.delete(intervals1,-1)
        freq1 = cumulative_freq

        freq2 = np.insert(cumulative_freq2,0,1)
        x2 = list(intervals2)

        res1 = pd.DataFrame({'x':x1,'y':freq1})
        res2 = pd.DataFrame({'x':x2,'y':freq2})

        lowess = sm.nonparametric.lowess
        y1 = lowess(res1['y'], res1['x'],frac=0.03)
        y2 = lowess(res2['y'], res2['x'],frac=0.03)

        T,Y,xnew,ynew1,ynew2 = find_t(y1[:,0],y2[:,0],y1[:,1],y2[:,1],interval=0.001)
        ntl = np.exp(T)-1
        rows.append([i,T,Y,ntl])
        print(i)

    df = pd.DataFrame(rows,columns=['id','T','Y','area'])
    df.to_csv(outdir+f'\\{tp}_mean.csv',index=False)

    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
