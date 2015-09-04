__author__ = 'alonsobarquero'

import os.path

from configs.config import LocustConfigs as MM


global_config="""
[global]
run_time = {}
rampup = {}
results_ts_interval = {}
progress_bar = {}
console_logging = {}
xml_report = {}
"""

user_group = """
[user_group-1]
threads = {}
script = {}
"""

try:
    with open("../config.cfg", "w") as f:
        # Writting Global Configs
        f.write(global_config.format(MM.RUN_TIME, MM.RAMPUP, MM.RESULTS_TS_INTERVAL,
                                     MM.PROGRESS_BAR, MM.CONSOLE_LOGGING, MM.XML_REPORT))
        # Setting User-group
        f.write(user_group.format(MM.THREADS, MM.TRANSACTION_FILE))
        print("Config file created successfully")

except:
    print("Unable to create Config file ...")

