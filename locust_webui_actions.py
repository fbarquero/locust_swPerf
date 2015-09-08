__author__ = 'alonsobarquero'
from time import sleep
from time import strftime
from requests import Session
import os

from configs.config import GlobalConfigs as GC


class LocustioWebActions:

    def __init__(self):
        self.session = Session()

    def get_stats_locust(self):
        response = self.session.get("http://localhost:8089/stats/requests")
        print("Stats/requests response: {}".format(response.content))


    def start_locust(self):
        if not os.path.exists(GC.RESULTS_BASE_PATH):
            os.makedirs(GC.RESULTS_BASE_PATH)
        current_date_time = "{}_{}".format(strftime("%x"), strftime("%X"))
        os.makedirs("{}/{}".format(GC.RESULTS_BASE_PATH, current_date_time))
        form_data = {"locust_count": 200, "hatch_rate": 10}
        response = self.session.post("http://localhost:8089/swarm", data=form_data)
        print("Response from start_locust: {}".format(response.content))


    def stop_locust(self):
        response = self.session.get("http://localhost:8089/stop")
        print("Response from stop: {}".format(response.content))

    def reset_locust(self):
        response = self.session.get("http://localhost:8089/stats/reset")
        print("Response from Reset stats: {}".format(response.content))


    def get_request_stats_csv(self):
        response = self.session.get("http://localhost:8089/stats/requests/csv")
        print("request stats csv: {}".format(response.content))


    def get_stats_distribution_csv(self):
        response = self.session.get("http://localhost:8089/stats/distribution/csv")
        print("request stats distribution csv: {}".format(response.content))


    def get_exceptions_csv(self):
        response = self.session.get("http://localhost:8089/exceptions/csv")
        print("request exception csv: {}".format(response.content))

    def save_locustio_basic_reports(self):
        if not os.path.exists(GC.RESULTS_BASE_PATH):
            os.makedirs(GC.RESULTS_BASE_PATH)
        current_date_time = "{}_{}".format(strftime("%x"), strftime("%X"))
        os.makedirs("{}/{}".format(GC.RESULTS_BASE_PATH, current_date_time))


