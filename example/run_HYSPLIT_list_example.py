import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import hysplit_runner.hysplit
import datetime as dt

STATION = "wuhan"
TASK_FILE = "C:\\Users\\zpyin\\Desktop\\trace\\output\\wuhan\\hysplit_input_wuhan_20191119_00.csv"

runner = hysplit_runner.hysplit.HYSPLIT(
    hysplit_exe_dir='C:\\hysplit4\\exec',
    hysplit_working_dir='C:\\hysplit4\\working\\',
    hysplit_tdump_dir='C:\\Users\\zpyin\\Desktop\\trace\\tdump\\wuhan\\'
)

# run ens mode
runner.run_HYSPLIT_list(
    TASK_FILE,
    meteor_dir='D:\\Data\\GDAS\\global', mode="ens", station="wuhan")
