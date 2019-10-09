# -*- coding: utf-8 -*-
"""
config file for HYSPLIT trajectory running and plotting
Created on Wed Apr 4 2018
@author: Johannes Mohrmann

recomposed by Zhenping
"""

# should be either 'windows' or 'linux'
OS = 'windows'

# working directory for HYSPLIT to write CONTROL file. need write access
HYSPLIT_working_dir = 'C:\\hysplit4\\working' 
# write directory for HYSPLIT output files. need write access (can be anywhere)
HYSPLIT_tdump_dir = 'C:\\hysplit4\\working'
# pathname for HYSPLIT executable. need execute access
HYSPLIT_call = 'C:\\hysplit4\\exec\\hyts_std.exe'
# write directory for saving plots
plot_dir = 'D:\\MUA\\model\\hysplit\\backward_trajectory'
# read directory for HYSPLIT data. This shouldn't need changing unless you're downloading analysis I don't have
HYSPLIT_source_dir = 'D:\\MUA\\model\\gdas0p5_global'
# write directory for geostationary imagery
imagery_dir = 'D:\\MUA\\satellite\\geostationary_image'

# default display range for the satellite image
latlon_range = {'lat': [-90, 90], 'lon': [-180, 180]}