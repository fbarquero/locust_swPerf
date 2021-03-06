from locust import HttpLocust, TaskSet, task, events
import sys
import pickle
import os
from BeautifulSoup import BeautifulSoup
from requests.adapters import HTTPAdapter
from time import time

from configs.config import LocustConfigs as locust_config
from configs.config import ProxyConfigs as proxy_config
from configs.config import GlobalConfigs as GC
from utilities import sw_user_management as usrs
from sw_requests.sowatest import SowatestRequests
from custom_runner import custom_runner as c_runner


if locust_config.USE_PROXY:
    print("Loading user sessions ...\n")
    users_pool = usrs.load_sessions_pickle()
    print("\nUsers loaded successfully\n")

print("\nLoading swPerf config information\n")
c_runner.load_swperf_config_data()
print("\nswPerf config loaded sucessfully")


class UserBehavior(TaskSet):

    @task
    def hit_sowatest(self):
        try:
            if locust_config.USE_PROXY:
                user_credentials = users_pool.pop(0)
                http_adapter = HTTPAdapter(max_retries=0)
                self.client.mount('http://', http_adapter)
                self.client.mount('https://', http_adapter)
                proxy_request = SowatestRequests(self.client)
                response = proxy_request.sowatest_through_proxy(user_credentials)
                # soup = BeautifulSoup(response.text)
                # Assert Section
                # assert response.status_code is 200, "unexpected response status code {}".format(response.status_code)
                # assert "Access Denied" in str(soup.find("title").text)
                # assert '<div id="blockedBanner">' in response.text
            else:
                print("no proxy")
        except Exception, e:
            # if locust_config.USE_PROXY:
            #     if e.message is 'location':
            #         raise Exception('Possible authentication error against IDP!')
            #     raise
            pass
        finally:
            if locust_config.USE_PROXY:
                users_pool.append(user_credentials)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 0
    host = "http://sowatest.com"
    stop_timeout = locust_config.RUN_TIME


def on_master_start_hatching():
    info = dict(pid=os.getpid(), start_time=time(), ramp_up=True)
    with open(GC.STARTING_INFO_FILE_PATH, "wb") as f:
        pickle.dump(info, f)
    print info


def on_hatch_complete(user_count):
    info = dict(pid=os.getpid(), start_time=time(), ramp_up=False)
    with open(GC.STARTING_INFO_FILE_PATH, "wb") as f:
        pickle.dump(info, f)
    print info

events.master_start_hatching += on_master_start_hatching
events.hatch_complete += on_hatch_complete






