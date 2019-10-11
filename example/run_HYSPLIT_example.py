from hysplit_runner.hysplit_runner import HYSPLIT
import datetime as dt

STATION = "wuhan"

runner = HYSPLIT(
    hysplit_exe_dir='/Users/yinzhenping/Hysplit4/exec',
    hysplit_working_dir='/Users/yinzhenping/Hysplit4/working',
    hysplit_tdump_dir='/Users/yinzhenping/Desktop/trace/output/wuhan'
)

# run std mode
runner.run_HYSPLIT(
    dt.datetime(2018, 4, 11), [(34, 114)], -144, 0, [3500],
    meteor_source='GDAS1',
    meteor_dir='/Users/yinzhenping/Documents/TROPOS/data/GDAS/arielle/global',
    tdump_file='{}_std.tdump'.format(STATION),
    mode='std'
)

# run ens mode
runner.run_HYSPLIT(
    dt.datetime(2018, 4, 11), [(34, 114)], -144, 0, [3500],
    meteor_source='GDAS1',
    meteor_dir='/Users/yinzhenping/Documents/TROPOS/data/GDAS/arielle/global',
    tdump_file='{}_ens.tdump'.format(STATION),
    mode='ens'
)
