"""
Generate a dataset of guitar dry signals. This is a ReaScript for the Reaper.
"""

import dataset_config as dat
import reaper_python as rp
import time
import os
import shutil

start = time.time()
data_num = 0  # Serial number of the data
if os.path.exists(dat.dataset_path / "data"):
    shutil.rmtree(dat.dataset_path / "data")
for guitar in dat.guitars.keys():
    for string in dat.strings:
        for fret in dat.frets:
            guitar_info = dat.GuitarInfo(guitar, string, fret)
            dat.make_data(guitar_info, data_num)
            data_num += 1
end = time.time()
rp.RPR_ShowConsoleMsg("execute time: " + str(end - start) + "sec")
