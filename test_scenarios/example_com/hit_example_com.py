from locust import HttpLocust, TaskSet, task, events
import pickle
import os
from time import time

from configs.config import LocustConfigs as locust_config
from configs.config import GlobalConfigs as GC




class UserBehavior(TaskSet):

    @task
    def test_example_no_proxy(self):
        self.client.get("/", timeout=10)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 0
    host = "http://www.example.com"
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






