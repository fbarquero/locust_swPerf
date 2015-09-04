__author__ = 'alonsobarquero'


import argparse

from custom_runner import custom_runner
from utilities import sw_user_management as users

parser = argparse.ArgumentParser(description='Executes Socialware performance project.')
required = parser.add_argument_group("Required arguments:")
required.add_argument('-u', type=int, nargs=1, required=True, help='Number of users to simulate for Performance '
                                                                   '/ Load Testing')
required.add_argument('-f', type=str, nargs=1, required=True, help='Locust file for Performance / Load Testing')
required.add_argument('-t', type=int, nargs=1, required=True, help='Time for the Performance/Load tests to '
                                                                   'run in seconds')
required.add_argument('-r', type=int, nargs=1, required=True, help='How many users you want to ramp-up per second')

required.add_argument("-l", choices=["once", "all", "none"], nargs=1, required=True, help="Login style required for the"
                                                                                          " test")
optional = parser.add_argument_group("Non-required arguments:")
optional.add_argument("--print-stats", help="Console logging activated turn it on for debugging purposes only",
                      action="store_true")
optional.add_argument("--summary-only", help="Displays only the summary after the execution ends",
                      action="store_true")
optional.add_argument("--request-timeout", default=[5], type=int, nargs=1, help="Global request timeout for all the "
                                                                              "transactions executed in the tests "
                                                                              "(default is 5 seconds)")
optional.add_argument("--no-web", help="disable web view for Locust",
                      action="store_true")
# Parse arguments
args = parser.parse_args()

# Store multi-mechanize configuration info after parse args
locust_config_info = {}


def parse_args_to_dict():
    """
    Store the arguments parsed with argsparse in a dictionary
    :return: Dictionary with all the info got from the arguments parsed
    """
    locust_config_info["run_time"] = args.t[0]
    locust_config_info["ramp_up"] = args.r[0]
    locust_config_info["print_stats"] = args.print_stats
    locust_config_info["summary_only"] = args.summary_only
    locust_config_info["users"] = args.u[0]
    locust_config_info["test_name"] = args.f[0]
    if args.l is "once":
        locust_config_info["login_style"] = "once"
    elif args.l is "all":
        locust_config_info["login_style"] = "all"
    elif args.l is "none":
        locust_config_info["login_style"] = "none"
    locust_config_info["request_timeout"] = args.request_timeout[0]
    locust_config_info["no_web"] = args.no_web
    return locust_config_info


print("Saving Locust config data...")
locust_data = parse_args_to_dict()
custom_runner.save_multi_mech_data_pickle(locust_data)
print("Saving process completed for Locust required data...\n")

print("Creating Multi-Mechanize config file")
custom_runner.create_mm_config_file(locust_data)

print("Creating user sessions for testing")
users.save_sessions_pickle(locust_config_info["users"])
print("user sessions created successfully...\n")
print("Starting Multi-mechanize execution for swPerf proyect: \n")

cmd = []
increase_max_open_files = custom_runner.get_os_max_file_config()
cmd.append("source env/bin/activate")
cmd.append("pip freeze -l")
if len(increase_max_open_files) > 0:
    cmd = cmd + increase_max_open_files
locust_run_cmd = "locust -f {} -c {} -r {}".format(locust_data["test_name"],
                                                   locust_data["users"],
                                                   locust_data["ramp_up"])
if locust_config_info["no_web"]:
    locust_run_cmd += " --no-web"
if locust_config_info["summary_only"]:
    locust_run_cmd += " --summary-only"
if locust_config_info["print_stats"]:
    locust_run_cmd += " --print-stats"
cmd.append(locust_run_cmd)
print(cmd)

# Run all CLI Commands needed to start multi - mechanize after configure the project
custom_runner.execute_cli_command(cmd)
