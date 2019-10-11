# HYSPLIT runner

python package for easily calling [HYSPLIT][1].

## Download

```text
git clone https://github.com/ZPYin/hysplit_runner.git
```

## Requirements

- Python 3.6
- HYSPLIT model

To make your life with [Python][2] easier, we highly recommend you to use [**Anaconda3**][3].

For HYSPLIT [installation][4], you only need to download the executive files, which would save you a lot of time with installing the Graphic User Interface (GUI). But you are free to install the GUI as well, since it doesn't have any interference with using the Python package.

## Usage

**python virtual environment**

```text
cd hysplit_runner

conda create -n hysplit_runner   # you can also choose other names for the virtual environment

# activate the virtual environment
activate hysplit_runner   # windows
source activate hysplit_runner   # MacOS or Linux

# install python and python packages
conda install python=3.6
pip install -r requirements.txt
```

**configure hysplit_runner**

and make sure you setup the correct paths for HYSPLIT model.

****







[1]: https://www.ready.noaa.gov/HYSPLIT.php
[2]: https://www.python.org
[3]: https://docs.anaconda.com
[4]: https://www.ready.noaa.gov/HYSPLIT_hytrial.php