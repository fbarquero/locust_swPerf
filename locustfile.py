from locust import Locust, TaskSet, task, events
from time import time
from BeautifulSoup import BeautifulSoup
import requests

from sw_requests.sowatest import SowatestRequests
from configs.config import MultiMechanizeConfigs as MM
from utilities import sw_user_management as usrs

##  locust -f locustfile.py --no-web -n 10 -r 10


# if MM.USE_PROXY:
#     print("Loading user sessions ...\n")
#     users_pool = usrs.load_sessions_pickle()
#     print("\nUsers loaded successfully\n")


class LocustTask(TaskSet):

    # @task
    # def hit_sowatest(self):
    #     try:
    #         if MM.USE_PROXY:
    #             self.start_time = time()
    #             user_credentials = users_pool.pop(0)
    #             proxy_request = SowatestRequests()
    #             response = proxy_request.sowatest_through_proxy(user_credentials)
    #             soup = BeautifulSoup(response.text)
    #             # Assert Section
    #             assert response.status_code is 200, "unexpected response status code {}".format(response.status_code)
    #             assert "Access Denied" in str(soup.find("title").text)
    #             assert '<div id="blockedBanner">' in response.text
    #             events.request_success.fire(request_type="Transaction", name="hit_sowatest", response_time=time() - self.start_time, response_length=0)
    #         else:
    #             print("no proxy")
    #     except Exception, e:
    #         if MM.USE_PROXY:
    #             if e.message is 'location':
    #                 raise Exception('Possible authentication error against IDP!')
    #                 events.request_failure.fire(request_type="Transaction", name="hit_sowatest", response_time=time() - self.start_time, exception='Possible authentication error against IDP!')
    #         events.request_failure.fire(request_type="Transaction", name="hit_sowatest", response_time=time() - self.start_time, exception=e.message)
    #     finally:
    #         if MM.USE_PROXY:
    #             users_pool.append(user_credentials)
    #             proxy_request.session.close()
    #

    @task
    def printing_someting(self):
        try:
            self.start_time = time()
            session = requests.Session()
            session.get("http://www.example.com", timeout=5)
            # # print("Doing a task that is not a request...")
            # login = Login()
            # r = login.sw_valid_login(GC.USERNAME, GC.PASSWORD, "http://www.sowatest.com")
            stats_latency['latency'].append(time() - self.start_time)
            events.request_success.fire(request_type="Transaction", name="hit_sowatest", response_time=time() - self.start_time, response_length=0)

            # # Assert Section
            # assert r.status_code == 200
            # assert "Access Denied" in str(html.fromstring(r.text).xpath("//title/text()"))
            # assert '<div id="blockedBanner">' in r.text
        except Exception, e:
            """
            * *request_type*: Request type method used
            * *name*: Path to the URL that was called (or override name if it was used in the call to the client)
            * *response_time*: Time in milliseconds until exception was thrown
            * *exception*: Exception instance that was thrown
            """
            events.request_failure.fire(request_type="Transaction", name="hit_sowatest", response_time=time() - self.start_time, exception=e.message)

class ConsoleUser(Locust):
    task_set = LocustTask
    min_wait = 5*1000
    max_wait = 15*1000
    stop_timeout = MM.RUN_TIME


"""
Gattering global stats to generate reports
"""
stats_latency = {"latency":[], "success": [], "failure": []}
execution_started = time()
transaction_p = 0
transaction_f = 0


def on_request_success(request_type, name, response_time, response_length):
    """
    Event handler that get triggered on every successful request
    """
    stats_latency["success"].append(dict(request_type=request_type, name=name, response_time=response_time, response_length=response_length))
    global transaction_p
    transaction_p += 1


def on_request_failure(request_type, name, response_time, exception_message):
    """
    Event handler that get triggered on every failed request
    """
    stats_latency["failure"].append(dict(request_type=request_type, name=name, response_time=response_time, exception=exception_message))
    global transaction_f
    transaction_f += 1


def on_hach_completed(user_count):
    print user_count
    global stats_latency
    stats_latency = {"latency": [], "success": [], "failure": []}
    global execution_started
    execution_started = time()
    global transaction_p
    transaction_p = 0
    global transaction_f
    transaction_f = 0


def on_quitting():
    total_transactions = transaction_p + transaction_f
    print("Printing My stats:\n")
    # print(stats_latency)
    print("success: {}".format(transaction_p))
    print("failed: {}".format(transaction_f))
    latency_p = 0
    latency_f = 0
    for transaction in stats_latency["success"]:
        latency_p += transaction["response_time"]
    for transaction in stats_latency["failure"]:
        latency_f += transaction["response_time"]
    total_latency = latency_p + latency_f
    if latency_p > 0:
        print("Average latency for succeded transactions: {}".format(latency_p/float(transaction_p)))
    if latency_f > 0:
        print("Average latency for failed transactions: {}".format(latency_p / float(transaction_f)))
    print("Average latency all transactions: {}".format((total_latency) / float(total_transactions)))

    # print("stats_latency['latency'] len: {}".format(len(stats_latency['latency'])))
    print("Total Transactions: {}".format(total_transactions))
    print("Transactions per second: {}".format(total_transactions / float(MM.RUN_TIME)))

# Hook up the event listeners
events.request_success += on_request_success
events.request_failure += on_request_failure
events.quitting += on_quitting
events.hatch_complete += on_hach_completed

