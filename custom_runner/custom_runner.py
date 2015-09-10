__author__ = 'alonsobarquero'
import pickle
import subprocess
from sys import platform as _platform


from configs.config import GlobalConfigs as GC
from configs.config import LocustConfigs as locust_config


def save_multi_mech_data_pickle(multi_mech_data):
    '''
    save multi-mechanize configuration dictionary in an obj file
    :param multi_mech_data:
    :return:
    '''
    if multi_mech_data is not None:
        with open(GC.MULTI_MECH_FILE_PATH, "wb") as f:
            pickle.dump(multi_mech_data, f)
    else:
        raise Exception("Problems loading data ...")


def load_multi_mech_data():
    '''
    Load multi-mechanize config values dictionary from multi_mech_data.obj
    :return:
    '''
    with open(GC.MULTI_MECH_FILE_PATH, "rb") as f:
        multi_mech_data = pickle.load(f)
    if not isinstance(multi_mech_data, dict):
        raise Exception("Data not loaded as expected... Data: {}".format(multi_mech_data))
    return multi_mech_data


def create_mm_config_file(mm_data):
    '''
    Recreate multi-mechanize default config.cfg file with the arguments gathered from our
    custom runner
    :param mm_data: Multi-Mechanize config data from custom runner
    :return:
    '''
    global_config = """
[global]
run_time = {}
rampup = {}
results_ts_interval = {}
progress_bar = {}
console_logging = {}
xml_report = {}
"""

    user_group = """
[user_group-{}]
threads = {}
script = {}
"""

    try:
        print("Config file path:\n{}".format(locust_config.CONFIG_FILE_PATH))
        with open(locust_config.CONFIG_FILE_PATH, "w") as f:
            # Writting Global Configs
            global_config_formatted = global_config.format(mm_data["run_time"], mm_data["ramp_up"],
                                                           mm_data["results_ts_interval"],
                                                           mm_data["progress_bar"], mm_data["console_logging"],
                                                           mm_data["xml_report"])
            f.write(global_config_formatted)
            user_groups = mm_data["threads"] // GC.GROUPS_OF
            last_group = mm_data["threads"] - (user_groups * GC.GROUPS_OF)
            for x in xrange(1, user_groups + 1):
                user_group_formatted = user_group.format(x, GC.GROUPS_OF, mm_data["test_name"])
                # Setting User-group
                f.write(user_group_formatted)
            if last_group > 0:
                user_group_formatted = user_group.format(user_groups + 1, last_group, mm_data["test_name"])
                f.write(user_group_formatted)
        print("Config file created successfully\n")
    except:
        print("Unable to create Config file ...")


def execute_cli_command(commands):
    """
    Execute cli commands and print the output in terminal
    :param commands: list of command lines to execute in a list object
    :return:
    """
    cmd = ""
    for command in commands:
        cmd += str("{};".format(command))
    process = subprocess.Popen(cmd, shell=True)
    process.communicate()
    output = process.communicate()[0]
    exit_code = process.returncode

    if exit_code != 0:
        raise Exception(command, exit_code, output)
    return output


def load_swperf_config_data():
    """
    Modifies the swPer config file adding the values gathered from
    custom runner arguments
    :return:
    """
    mm_data = load_multi_mech_data()
    locust_config.RUN_TIME = mm_data["run_time"]
    locust_config.RAMPUP = mm_data["ramp_up"]
    locust_config.USERS = mm_data["users"]
    locust_config.TRANSACTION_FILE = mm_data["test_name"]
    GC.GLOBAL_REQUEST_TIMEOUT = mm_data["request_timeout"]


def get_os_platform():
    return _platform


def get_os_max_file_config():
    cmd = []

    # if "linux" in _platform:
    #     cmd.append("sudo sysctl -w fs.file-max={}".format(GC.MAX_OPEN_FILES))
    #     cmd.append("ulimit -Sn {}".format(GC.MAX_OPEN_FILES))
    #     cmd.append("ulimit -Hn {}".format(GC.MAX_OPEN_FILES))
    if "darwin" in _platform:
        print("Increasing Open File Limit for current OS \"{}\"..".format(_platform))
        cmd.append("sudo sysctl -w kern.maxfiles={}".format(GC.MAX_OPEN_FILES))
        cmd.append("sudo sysctl -w kern.maxfilesperproc={}".format(GC.MAX_OPEN_FILES))
        cmd.append("ulimit -S -n {}".format(GC.MAX_OPEN_FILES))
    return cmd



