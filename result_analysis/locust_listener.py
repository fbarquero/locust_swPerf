__author__ = 'alonsobarquero'
import os
import pickle
from requests import Session
from time import sleep
from time import strftime
from time import time
import json

from configs.config import GlobalConfigs as GC
from configs.config import LocustConfigs as LC
from locust_actions.locust_webui_actions import LocustioWebActions


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
        result_folder = locust_web_actions.start_locust()
        locust_starting_info = locust_web_actions.get_starting_info()

        request_stats_csv = "{}/{}".format(result_folder, "request_stats.csv")
        stats_distribution_csv = "{}/{}".format(result_folder, "stats_distribution.csv")
        exceptions_csv = "{}/{}".format(result_folder, "exceptions.csv")

        request_failed = []
        num_requests = []
        median_response_time = []
        average_response_time = []
        max_response_time = []
        request_per_second = []
        print time() - locust_starting_info["start_time"]

        while time() - locust_starting_info["start_time"] < (LC.RUN_TIME + 5):
            stats = json.loads(self.get_stats_locust())
            stat = stats["stats"][0]
            request_failed.append(stat["num_failures"])
            num_requests.append(stat["num_requests"])
            request_per_second.append(round(stat["current_rps"], 2))
            median_response_time.append(round(stat["median_response_time"], 2))
            average_response_time.append(round(stat["avg_response_time"], 2))
            max_response_time.append(round(stat["max_response_time"], 2))
            sleep(1)
        with open(request_stats_csv, "w") as f:
            f.write(locust_web_actions.get_request_stats_csv())
        with open(stats_distribution_csv, "w") as f:
            f.write(locust_web_actions.get_stats_distribution_csv())
        with open(exceptions_csv, "w") as f:
            f.write(locust_web_actions.get_exceptions_csv())
        print("requests: {}".format(num_requests))
        print("request_failed: {}".format(request_failed))
        print("request per second: {}".format(request_per_second))
        locust_web_actions.kill_master()


ResultGathering().listening_locust_stats()
