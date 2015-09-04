from locust import HttpLocust, TaskSet, task
from BeautifulSoup import BeautifulSoup

from configs.config import LocustConfigs as locust_config
from configs.config import ProxyConfigs as proxy_config
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

    # @task
    # def hit_sowatest(self):
    #     try:
    #         if locust_config.USE_PROXY:
    #             user_credentials = users_pool.pop(0)
    #             proxy_request = SowatestRequests(self.client)
    #             response = proxy_request.sowatest_through_proxy(user_credentials)
    #             # soup = BeautifulSoup(response.text)
    #             # Assert Section
    #             # assert response.status_code is 200, "unexpected response status code {}".format(response.status_code)
    #             # assert "Access Denied" in str(soup.find("title").text)
    #             # assert '<div id="blockedBanner">' in response.text
    #         else:
    #             print("no proxy")
    #     except Exception, e:
    #         if locust_config.USE_PROXY:
    #             if e.message is 'location':
    #                 raise Exception('Possible authentication error against IDP!')
    #             raise
    #     finally:
    #         if locust_config.USE_PROXY:
    #             users_pool.append(user_credentials)
    @task
    def test_proxy(self):
        user_credentials = users_pool.pop(0)
        response = self.client.cookies = user_credentials[1]
        self.client.get("/", proxies=proxy_config.PROXIES, verify=False)
        users_pool.append(user_credentials)
        print response.content


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 200
    host = "http://sowatest.com"
    stop_timeout = locust_config.RUN_TIME




