from locust import HttpLocust, TaskSet, task
from BeautifulSoup import BeautifulSoup
from requests.adapters import HTTPAdapter

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
    # @task
    # def test_proxy(self):
    #     user_credentials = users_pool.pop(0)
    #     self.client.cookies = user_credentials[1]
    #     response = self.client.get("/", proxies=proxy_config.PROXIES, verify=False)
    #     users_pool.append(user_credentials)
    #     print response.content
    #
    # @task
    # def test_example(self):
    #     user_credentials = users_pool.pop(0)
    #     self.client.cookies = user_credentials[1]
    #     response = self.client.get("/", proxies=proxy_config.PROXIES, verify=False)
    #     users_pool.append(user_credentials)
    #     print response.content

    # @task
    # def test_example_through_proxy(self):
    #     user_credentials = users_pool.pop(0)
    #     proxy_request = SowatestRequests(self.client)
    #     proxy_request.example_through_proxy()
    #     users_pool.append(user_credentials)

    #
    # @task
    # def test_example_no_proxy(self):
    #     self.client.get("/", timeout=10)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 0
    # host = "http://sowatest.com"
    host = "http://sowatest.com"
    stop_timeout = 1800




