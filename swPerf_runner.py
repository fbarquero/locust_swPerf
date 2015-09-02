#!/usr/local/bin/python
__author__ = 'alonsobarquero'

import argparse

from custom_runner import custom_runner
from utilities import sw_user_management as users

parser = argparse.ArgumentParser(description='Executes Socialware performance project.')
required = parser.add_argument_group("Required arguments:")
required.add_argument('-u', type=int, nargs=1, required=True, help='Number of users to simulate for Performance '
                                                                   '/ Load Testing')
required.add_argument('-tn', type=str, nargs=1, required=True, help='Test name to use for Performance / Load Testing')
required.add_argument('-t', type=int, nargs=1, required=True, help='Time for the Performance/Load tests to '
                                                                   'run in seconds')
required.add_argument('-r', type=int, nargs=1, required=True, help='Users rampup time in seconds')
required.add_argument("-rtsin", type=int, nargs=1, required=True, help="Set result ts interval i.e -rtsin 30 will set "
                                                                       "interval to 30 seconds")
required.add_argument("-l", choices=["once", "all", "none"], nargs=1, required=True, help="Login style required for the"
                                                                                          " test")
optional = parser.add_argument_group("Non-required arguments:")
optional.add_argument("--verbose", help="Console logging activated turn it on for debugging purposes only",
                      action="store_true")
optional.add_argument("--no-progress-bar", help="Display progress bar",
                      action="store_true")
optional.add_argument("--xml-report", action="store_true", help="Enables the creation of JTL Jenkins execution report")
optional.add_argument("--request-timeout", default=[5], type=int, nargs=1, help="Global request timeout for all the "
                                                                              "transactions executed in the tests "
                                                                              "(default is 5 seconds)")
# Parse arguments
args = parser.parse_args()

# Store multi-mechanize configuration info after parse args
multi_mech_config_info = {}


def parse_args_to_dict():
    """
    Store the arguments parsed with argsparse in a dictionary
    :return: Dictionary with all the info got from the arguments parsed
    """
    multi_mech_config_info["run_time"] = args.t[0]
    multi_mech_config_info["results_ts_interval"] = args.rtsin[0]
    multi_mech_config_info["rampup"] = args.r[0]
    if args.no_progress_bar:
        multi_mech_config_info["progress_bar"] = "off"
    else:
        multi_mech_config_info["progress_bar"] = "on"
    if args.verbose:
        multi_mech_config_info["console_logging"] = "on"
    else:
        multi_mech_config_info["console_logging"] = "off"
    if args.xml_report:
        multi_mech_config_info["xml_report"] = "on"
    else:
        multi_mech_config_info["xml_report"] = "off"
    multi_mech_config_info["threads"] = args.u[0]
    multi_mech_config_info["test_name"] = args.tn[0]
    if args.l is "once":
        multi_mech_config_info["login_style"] = "once"
    elif args.l is "all":
        multi_mech_config_info["login_style"] = "all"
    elif args.l is "none":
        multi_mech_config_info["login_style"] = "none"
    multi_mech_config_info["request_timeout"] = args.request_timeout[0]
    return multi_mech_config_info


print("Saving Multi-Mechanize config data...")
multimech_data = parse_args_to_dict()
custom_runner.save_multi_mech_data_pickle(multimech_data)
print("Saving process completed for Multi-Mechanize required data...\n")

print("Creating Multi-Mechanize config file")
custom_runner.create_mm_config_file(multimech_data)

print("Creating user sessions for testing")
users.save_sessions_pickle(multi_mech_config_info["threads"])
print("user sessions created successfully...\n")
print("Starting Multi-mechanize execution for swPerf proyect: \n")

cmd = []
increase_max_open_files = custom_runner.get_os_max_file_config()
#cmd.append("cd ..")
cmd.append("source env/bin/activate")
if len(increase_max_open_files) > 0:
    cmd = cmd + increase_max_open_files
cmd.append("locust -f {} -c {} -r {} --no-web --print-stats".format(multimech_data["test_name"],
                                                                    multimech_data["threads"],
                                                                    multimech_data["rampup"]))
print(cmd)

# Run all CLI Commands needed to start multi - mechanize after configure the project
custom_runner.execute_cli_command(cmd)
