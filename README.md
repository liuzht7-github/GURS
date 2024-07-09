# GURS
Global Urban and Rural Settlement

#Purposes of each script:

s1: Extract potential settlement pixels from GHS-BUILT-S R2023A.
s2: Aggregate adjacent pixels into settlement patches.
s3: Calculate the area and brightness (Nighttime Lights) of settlement patches.
s4-6: Aggregate 375 blocks into 9 subregions.
s7.1: Extract points of urban settlements and rural settlements from osm_place and match them with settlement patches for statistical sample collection.
s7.2-7.4: Used for outlier removal, 100-time sampling, and threshold determination.
s8 and s9: Divide settlement patches into urban settlements and rural settlements based on thresholds and classification schemes, obtaining the initial global  urban and rural settlement map.
s10: Post-proscess to address spatial extent mismatch across multi-source data.
s11: Post-proscess to ensure logically consistent time-series data.
