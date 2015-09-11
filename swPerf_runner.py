__author__ = 'alonsobarquero'


import argparse
from custom_runner import custom_runner
from utilities import sw_user_management as users
from result_analysis.locust_listener import ResultGathering

parser = argparse.ArgumentParser(description='Executes Socialware performance project.')
required = parser.add_argument_group("Required arguments:")
required.add_argument('-u', type=int, nargs=1, required=True, help='Number of users to simulate for Performance '
                                                                   '/ Load Testing')
required.add_argument('-f', type=str, nargs=1, required=True, help='Locust file for Performance / Load Testing')
required.add_argument('-t', type=int, nargs=1, required=True, help='Time for the Performance/Load tests to '
                                                                   'run in seconds')
required.add_argument('-r', type=int, nargs=1, required=True, help='How many users you want to ramp-up per second')
required.add_argument('-tsin', type=int, nargs=1, required=True, help='Time series interval for Charts')

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
optional.add_argument("--create-user-sessions", help="create user sessions for the concurrent users that will be swarmed",
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
    locust_config_info["tsin"] = args.tsin[0]
    print "login style: {} l[0]: {}".format(args.l, args.l[0])
    locust_config_info["login_style"] = args.l[0]
    locust_config_info["request_timeout"] = args.request_timeout[0]
    return locust_config_info


print("Saving Locust config data...")
locust_data = parse_args_to_dict()
custom_runner.save_multi_mech_data_pickle(locust_data)
print("Saving process completed for Locust required data...\n")

if args.create_user_sessions:
    print("Creating user sessions for testing")
    users.save_sessions_pickle(locust_config_info["users"])
    print("user sessions created successfully...\n")

print("\nLoading swPerf config information\n")
custom_runner.load_swperf_config_data()
print("\nswPerf config loaded sucessfully")

print("Test Summary: ")
print("Amount of concurrent Users: {}".format(locust_config_info["users"]))
print("Users Ramp-up per second: {}".format(locust_config_info["ramp_up"]))
print("Run time: {}".format(locust_config_info["run_time"]))
print("Results Time Series Interval: {}".format(locust_config_info["tsin"]))
print("Login style: {}".format(locust_config_info["login_style"]))
print("Locust file to use: {}".format(locust_config_info["test_name"]))
print("Create user sessions: {}".format(args.create_user_sessions))

ResultGathering().listening_locust_stats()

