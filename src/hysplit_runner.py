# -*- coding: utf-8 -*-
"""
Hysplit runner.

2019-10-06 Modified by Zhenping Yin
"""

import os
import sys
import glob
import re
import toml
import fnmatch
import datetime as dt
import numpy as np
from subprocess import check_call
from logger_init import logger_def
import csv


PROJECTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIGFILE = os.path.join(PROJECTDIR, 'config', 'config.toml')
logger = logger_def()

# load default configurations
with open(CONFIGFILE, 'r', encoding='utf-8') as fh:
    CONFIG = toml.loads(fh.read())


def daterange(date1, date2):
    """"
    Create iteration between two dates.

    Reference
    ---------
    https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-50.php
    """
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + dt.timedelta(n)


class HysplitRunner(object):
    """
    HYSPLIT trajectory model runner.
    """

    def __init__(self, *args,
                 hysplit_exe_dir=CONFIG['HYSPLIT']['EXE_DIR'],
                 hysplit_working_dir=CONFIG['HYSPLIT']['WORKING_DIR'],
                 hysplit_tdump_dir=CONFIG['HYSPLIT']['TDUMP_DIR']):

        self.hysplit_exe_dir = hysplit_exe_dir
        self.hysplit_working_dir = hysplit_working_dir
        self.hysplit_tdump_dir = hysplit_tdump_dir

    def write_control_file(self, start_time, coords, meteor_list, hours,
                           vertical_type, init_height, *args,
                           tdump_file=''):
        """
        Setup the CONTROL file for HYSPLIT model.

        Parameters
        ----------
        start_time: datetime obj

        coords: list of tuple (lat, lon)

        meteor_list: list
        list of meteorological data files used for the trajectory.

        hours: integer
        time span for the trajectory (negative for backward)

        vertical_type: integer
            0 'data' ie vertical velocity fields
            1 isobaric
            2 isentropic
            3 isopycnal (constant density)
            4 isohypsic (constant internal sigma coord)
            5 from velocity divergence
            6 something wacky to convert from msl to HYSPLIT's above ground level
            7 spatially averaged vertical velocity

        init_height: list
        ending height list for each coordinate. [m]

        Keywords
        --------
        tdump_file: str
        filename of the output results

        History
        -------
        2019-10-06 First edition by Zhenping
        """

        # CONTROL file path
        fl = os.path.join(self.hysplit_working_dir, 'CONTROL')

        with open(fl, 'w') as fh:

            fh.write(start_time.strftime('%y %m %d %H\n'))
            fh.writelines([str(len(init_height)), '\n'])
            for height in init_height:
                fh.write('{} {} {}\n'.format(
                    str(coords[0][0]),
                    str(coords[0][1]),
                    str(height))
                    )

            fh.writelines([str(hours), '\n'])

            fh.writelines([str(vertical_type), '\n', '12000.0\n'])

            fh.write('{}\n'.format(len(meteor_list)))
            for meteorFile in meteor_list:
                fh.writelines([
                    os.path.dirname(meteorFile), os.sep, '\n',
                    os.path.basename(meteorFile), '\n'])

            fh.writelines([self.hysplit_tdump_dir,
                           os.sep, '\n', tdump_file, '\n'])

        return os.path.join(self.hysplit_tdump_dir, tdump_file)

    def _search_meteor_file(self, start_time, stop_time, *args,
                            meteor_source='GDAS1', meteor_dir):
        """
        setup the meteorological file list.

        History
        -------
        2019-10-06 First edition by Zhenping.
        """

        def gdas1_fname_from_date(dt):
            """
            Return the GDAS1 filename with the given datetime.
            """
            months = {1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr',
                      5: 'may', 6: 'jun', 7: 'jul', 8: 'aug',
                      9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'}
            week_no = ((dt.day-1)//7)+1

            return 'gdas1.{}{}.w{}'.format(
                months[dt.month],
                dt.strftime('%y'),
                week_no
                )

        start_time_list = [date for date in daterange(start_time, stop_time)]
        meteor_files = list(
            set([gdas1_fname_from_date(dt) for dt in start_time_list])
            )

        filtered_meteor_files = []
        saved_meteor_files = os.listdir(meteor_dir)
        flagMatched = False
        for meteor_file in meteor_files:
            flagMatched = False
            for saved_meteor_file in saved_meteor_files:
                if fnmatch.fnmatch(saved_meteor_file, meteor_file):
                    filtered_meteor_files.append(
                        os.path.join(
                                        meteor_dir,
                                        saved_meteor_file
                                    )
                    )

                    # found the meteor_file in your local directory
                    flagMatched = True

            if not flagMatched:
                logger.error('{} cannot be found. Please download it'.
                             format(meteor_file))
                raise FileNotFoundError

        return filtered_meteor_files

    def run_HYSPLIT_std(self):
        """
        run single HYSPLIT trajectory.
        """

        with open(os.devnull, 'w') as FNULL:
            try:
                check_call(
                           os.path.join(self.hysplit_exe_dir, 'hyts_std.exe'),
                           shell=False,
                           cwd=self.hysplit_working_dir,
                           stdout=FNULL
                        )
            except Exception as e:
                logger.error('Failure in running HYSPLIT std.')
                return False

        return True

    def run_HYSPLIT_ens(self):
        """
        run HYSPLIT ensemble trajectory.
        """

        # prepare the SETUP.CFG
        setupFile = os.path.join(self.hysplit_working_dir, 'SETUP.CFG')
        with open(setupFile, 'w', encoding='utf-8') as fh:
            fh.writelines("""
                &SETUP
                KMSL=0,
                tm_rain=1,
                tm_tpot=0,
                tm_tamb=1,
                tm_mixd=1,
                tm_relh=1,
                tm_terr=1,
                dxf=0.4,
                dyf=0.4,
                dzf=0.008,
                /
            """)

        # prepare the TRAJ.CFG
        trajFile = os.path.join(self.hysplit_working_dir, 'TRAJ.CFG')
        with open(trajFile, 'w', encoding='utf-8') as fh:
            fh.writelines("""
                &SETUP
                tratio = 0.75,
                delt = 0.0,
                mgmin = 10,
                khmax = 9999,
                kmixd = 0,
                kmsl = 0,
                k10m = 1,
                nstr = 0,
                mhrs = 9999,
                nver = 0,
                tout = 60,
                tm_pres = 1,
                tm_tpot = 0,
                tm_tamb = 1,
                tm_rain = 1,
                tm_mixd = 1,
                tm_relh = 1,
                tm_sphu = 0,
                tm_mixr = 0,
                tm_dswf = 0,
                tm_terr = 1,
                dxf = 0.40,
                dyf = 0.40,
                dzf = 0.01,
                messg = 'MESSAGE',
                /
            """)

        # run the HYSPLIT model
        with open(os.devnull, 'w') as FNULL:
            try:
                check_call(
                           os.path.join(self.hysplit_exe_dir, 'hyts_ens.exe'),
                           shell=False,
                           cwd=self.hysplit_working_dir,
                           stdout=FNULL
                        )
            except Exception as e:
                logger.error('Failure in running HYSPLIT std.')
                return False

        return True

    def run_HYSPLIT(self, start_time, coords, hours, vertical_type,
                    init_height, *args,
                    meteor_source='GDAS1',
                    meteor_dir='',
                    tdump_file='',
                    mode='std'):

        """
        Run HYSPLIT.

        Parameters
        ----------
        start_time: datetime obj

        coords: list of tuple (lat, lon)

        hours: integer
        time span for the trajectory (negative for backward)

        vertical_type: integer
            0 'data' ie vertical velocity fields
            1 isobaric
            2 isentropic
            3 isopycnal (constant density)
            4 isohypsic (constant internal sigma coord)
            5 from velocity divergence
            6 something wacky to convert from msl to HYSPLIT's above ground level
            7 spatially averaged vertical velocity

        init_height: list
        ending height list for each coordinate. [m]

        Keywords
        --------
        meteor_source: str
        the meteorological data for running the model.

        meteor_dir: str
        directory for saving the meteorological data.

        tdump_file: str
        filename of the output results

        History
        -------
        2019-10-06 First edition by Zhenping
        """

        if not os.path.exists(meteor_dir):
            logger.error('{} does not exist.'.format(meteor_dir))
            raise FileNotFoundError

        # search the required meteorological data files
        meteorFileList = self._search_meteor_file(
            start_time + dt.timedelta(hours=hours),
            start_time,
            meteor_source=meteor_source,
            meteor_dir=meteor_dir
        )

        # setup the CONTROL file for the task
        self.write_control_file(start_time, coords, meteorFileList, hours,
                                vertical_type, init_height,
                                tdump_file=tdump_file)

        if mode is 'std':
            flag = self.run_HYSPLIT_std()
        elif mode is 'ens':
            flag = self.run_HYSPLIT_ens()
        else:
            logger.warning('Unknow HYSPLIT mode: {}'.format(mode))
            flag = False

    def run_HYSPLIT_list(self, taskFile, *args,
                         meteor_dir='', mode='ens'):
        """
        Run HYSPLIT with the given task list file.
        """

        if (not os.path.exists(taskFile)) or (not os.path.isfile(taskFile)):
            logger.warning('{} does not exist.'.format(taskFile))
            raise FileNotFoundError

        # read taskFile
        taskList = []
        with open(taskFile, 'r', encoding='utf-8') as fh:
            reader = csv.reader(fh)
            next(reader, None)
            taskList = [row for row in reader]

        # running the tasks
        for indx, task in enumerate(taskList):
            logger.info('Running task number: {0:05d}'.format(indx))

            year, month, day, hour, lat, lon, height, hours = task[0].split()
            year = int(year)
            month = int(month)
            day = int(day)
            hour = int(hour)
            lat = float(lat)
            lon = float(lon)
            height = float(height)
            hours = int(hours)
            ending_time = dt.datetime(year, month, day, hour)
            tdump_file = os.path.join(
                "limassol-{y:04d}{m:02d}{d:02d}-{h:02d}-{height:06.0f}_0{hours:04d}.tdump"
                .format(
                    y=year,
                    m=month,
                    d=day,
                    h=hour,
                    height=height,
                    hours=hours
                    )
            )

            self.run_HYSPLIT(ending_time, [(lat, lon)], hours, 0, [height],
                             meteor_source='GDAS1', meteor_dir=meteor_dir,
                             tdump_file=tdump_file, mode=mode)
            logger.info('{0:6.2f}% finished. '.format(
                (indx + 1)/len(taskList) * 100
            ))


def main():
    runner = HysplitRunner(hysplit_tdump_dir="C:\\Users\\zhenping\\Desktop\\hysplit_runner\\data\\tdump")
    # runner.run_HYSPLIT(dt.datetime(2019, 9, 1),
    #                    [(-30, 50)],
    #                    -144,
    #                    0,
    #                    [2000],
    #                    meteor_source='GDAS1',
    #                    meteor_dir='C:\\Users\\zhenping\\Documents\\Data\\GDAS\\global\\',
    #                    tdump_file='test1.tdump'
    #                    )
    runner.run_HYSPLIT_list('C:\\Users\\zhenping\\Desktop\\hysplit_runner\\data\\hysplit_input_limassol_20180314_00.csv',
     meteor_dir='C:\\Users\\zhenping\\Documents\\Data\\GDAS\\global\\')

if __name__ == '__main__':
    main()
