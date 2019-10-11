from hysplit_runner import HYSPLIT
import datetime as dt

STATION = "wuhan"

runner = HYSPLIT(
    hysplit_exe_dir='/Users/yinzhenping/Hysplit4/exec',
    hysplit_working_dir='/Users/yinzhenping/Hysplit4/workding',
    hysplit_tdump_dir='/Users/yinzhenping/Desktop/trace/output/wuhan'
)

runner.run_HYSPLIT(dt.datetime(2018, 3, 10), [(34, 114)], -144, 0, 3500,
                   meteor_source='GDAS1',
                   meteor_dir='/Users/yinzhenping/TROPOS/data/GDAS/global',
                   tdump_file='/Users/yinzhenping/Desktop/{}.tdump'.format(
                       STATION
                   ),
                   mode='std')
