__author__ = 'alonsobarquero'
import requests
from locust import TaskSet
requests.packages.urllib3.disable_warnings()

from sw_request_core.request import ProxyRequests
from configs.config import GlobalConfigs as GC


class SowatestRequests:

    def __init__(self, client):
        self.client = client

    def sowatest_through_proxy(self, credentials):
        proxy_request = ProxyRequests(self.client)
        self.client.cookies = credentials[1]
        response = proxy_request.get_with_proxy("/")
        return response

    def sowatest_no_proxy(self):
        response = self.client.get("/", timeout=GC.GLOBAL_REQUEST_TIMEOUT,
                                    verify=GC.VERIFY_CERTIFICATE)
        return response

    def example_through_proxy(self):
        proxy_request = ProxyRequests(self.client)
        r = proxy_request.get_with_proxy("/")
        return r

