import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import hysplit_runner.hysplit
import datetime as dt

STATION = "wuhan"

runner = hysplit_runner.hysplit.HYSPLIT(
    hysplit_exe_dir='C:\\hysplit4\\exec',
    hysplit_working_dir='C:\\hysplit4\\working\\',
    hysplit_tdump_dir='C:\\Users\\zpyin\\Desktop\\trace\\tdump'
)

runner.run_HYSPLIT(
    dt.datetime(2019, 11, 20), [(34, 114)], -144, 0, [3500],
    meteor_source='GDAS1',
    meteor_dir='D:\\Data\\GDAS\\global',
    tdump_file='{}.tdump'.format(STATION),
    mode='std')
