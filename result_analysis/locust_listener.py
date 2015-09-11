__author__ = 'alonsobarquero'
import os
import pickle
from requests import Session
from time import sleep
from time import strftime
from time import time
import json
import sys

from configs.config import GlobalConfigs as GC
from configs.config import LocustConfigs as LC
from locust_actions.locust_webui_actions import LocustioWebActions
from result_analysis import ResultAnalysis


class ResultGathering:
    def __init__(self):
        self.session = Session()

    def save_locustio_basic_report(self):
        if not os.path.exists(GC.RESULTS_BASE_PATH):
            os.makedirs(GC.RESULTS_BASE_PATH)
        current_date_time = "{}_{}".format(strftime("%x"), strftime("%X"))
        os.makedirs("{}/{}".format(GC.RESULTS_BASE_PATH, current_date_time))

    def get_stats_locust(self):
        response = self.session.get("http://localhost:8089/stats/requests")
        return response.content

    def listening_locust_stats(self):
        locust_web_actions = LocustioWebActions()
        result_analysis = ResultAnalysis()
        result_folder = locust_web_actions.start_locust()
        locust_starting_info = locust_web_actions.get_starting_info()
        graph_info = dict()
        request_failed = []
        num_requests = []
        median_response_time = []
        average_response_time = []
        max_response_time = []
        request_per_second = []
        ramp_up = True

        while ramp_up or time() - locust_starting_info["start_time"] < (LC.RUN_TIME + 1):
            sleep(1)
            stats = json.loads(self.get_stats_locust())
            stat = stats["stats"][0]
            request_failed.append(stat["num_failures"])
            num_requests.append(stat["num_requests"])
            request_per_second.append(round(stat["current_rps"], 2))
            median_response_time.append(
                round(0 if stat["median_response_time"] is None else stat["median_response_time"], 2))
            average_response_time.append(round(stat["avg_response_time"], 2))
            max_response_time.append(round(stat["max_response_time"], 2))
            if ramp_up:
                locust_starting_info = locust_web_actions.get_starting_info()
                if not locust_starting_info["ramp_up"]:
                    print("Ramp up is over")
                    # Saving ramp up information
                    graph_info["ramp_up_request_failed"] = result_analysis.compress_chart_dataset(request_failed)
                    graph_info["ramp_up_num_requests"] = result_analysis.compress_chart_dataset(num_requests)
                    graph_info["ramp_up_median_response_time"] = result_analysis.compress_chart_dataset(
                        median_response_time)
                    graph_info["ramp_up_average_response_time"] = result_analysis.compress_chart_dataset(
                        average_response_time)
                    graph_info["ramp_up_max_response_time"] = result_analysis.compress_chart_dataset(max_response_time)
                    graph_info["ramp_up_request_per_second"] = result_analysis.compress_chart_dataset(
                        request_per_second)
                    graph_info["ramp_up_time"] = len(num_requests)
                    graph_info["ramp_up_x_axis"] = result_analysis.get_chart_x_axis(len(num_requests))

                    # Cleaning ramp up info
                    request_failed = []
                    num_requests = []
                    median_response_time = []
                    average_response_time = []
                    max_response_time = []
                    request_per_second = []

                    ramp_up = locust_starting_info["ramp_up"]
            else:
                percent = float(time() - locust_starting_info["start_time"]) / LC.RUN_TIME
                hashes = '#' * int(round(percent * 20))
                spaces = ' ' * (20 - len(hashes))
                try:
                    failure_percentage = round(
                        float((stat["num_failures"] * 100)) / (stat["num_requests"] + stat["num_requests"]), 2)
                except Exception, e:
                    failure_percentage = 0
                sys.stdout.write(
                    "\rPercent: [{0}] {1}% Elapsed time: {5} Requests Succeded: {2}  Request Failed {3} ({4}%) "
                    "Total Requests: {6}".format(hashes + spaces, int(round(percent * 100)),
                                                 stat["num_requests"], stat["num_failures"],
                                                 failure_percentage,
                                                 round(time() - locust_starting_info["start_time"], 2),
                                                 stat["num_requests"] + stat["num_failures"]))
                sys.stdout.flush()
        locust_web_actions.kill_master()
        print("\nCompressing info for graphs")
        graph_info["request_failed"] = result_analysis.compress_chart_dataset(request_failed)
        graph_info["num_requests"] = result_analysis.compress_chart_dataset(num_requests)
        graph_info["median_response_time"] = result_analysis.compress_chart_dataset(median_response_time)
        graph_info["average_response_time"] = result_analysis.compress_chart_dataset(average_response_time)
        graph_info["max_response_time"] = result_analysis.compress_chart_dataset(max_response_time)
        graph_info["request_per_second"] = result_analysis.compress_chart_dataset(request_per_second)
        graph_info["x_axis"] = result_analysis.get_chart_x_axis(len(num_requests))
        graph_info["errors"] = stats["errors"]
        print("compression done")
        result_analysis.result_report(result_folder, graph_info)
