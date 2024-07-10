# Global urban and rural settlement dataset from 2000 to 2020

## Overview

This is the code repository for the research project "Global Urban and Rural Settlement Dataset from 2000 to 2020 (GRUS)." This work creates a global dataset of urban and rural settlements at a 100-meter resolution, based on open-source GHS-BUILT, OpenStreetMap, and NPP-VIIRS-like nighttime light data.  

The  dataset is available at  [here](https://zenodo.org/records/11160893). The dataset is stored in GeoTIFF format with the same coordinate reference system as GHS-BUILT, using the ESRI:54009 - World Mollweide projection. It employs an 8-bit unsigned integer format, where the pixels with a value of '1' represent urban settlements and '2' represent rural settlements. These data can be processed by ARCGIS, QGIS, MATLAB, and other tools.

## Script Description for Data Processing

The data processing for the GURS dataset involves several steps detailed in our paper. The scripts used for generating the dataset and analysis results were written in Python (3.9) and Arcpy (3.6). Here is a brief description of the related scripts:

- **s1:** Extract potential settlement pixels from the GHS-BUILT-S R2023A dataset.
- **s2:** Aggregate adjacent pixels to form larger settlement patches.
- **s3:** Calculate the area and brightness (using Nighttime Lights data) of each settlement patch.
- **s4-6:** Organize these patches into 375 blocks, further aggregating these into 9 subregions for detailed analysis.
- **s7.1:** Extract points representing urban and rural settlements from the 'osm_place' dataset and match these with the settlement patches for statistical sampling.
- **s7.2-7.4:** These scripts are utilized for outlier removal, repeated sampling (100 times), and determining the appropriate thresholds for classification.
- **s8 and s9:** Classify settlement patches into urban or rural categories based on the established thresholds and classification schemes, producing the preliminary global urban and rural settlement map.
- **s10:** Perform post-processing to correct any spatial extent mismatches that occur due to the integration of multi-source data.
- **s11:** Further post-process to ensure the logical consistency of the time-series data.