__author__ = 'alonsobarquero'
import requests
requests.packages.urllib3.disable_warnings()

from sw_request_core import request as r
from configs.config import GlobalConfigs as GC


class SowatestRequests:
    def __init__(self):
        self.session = None

    def sowatest_through_proxy(self, credentials):
        self.session = requests.Session()
        self.session.cookies = credentials[1]
        response = r.get_with_proxy(self.session, GC.SOCIAL_NETWORKING_URLs['direct_sowatest'])
        return response

    def sowatest_no_proxy(self):
        self.session = requests.Session()
        response = self.session.get(GC.SOCIAL_NETWORKING_URLs["direct_sowatest"], timeout=GC.GLOBAL_REQUEST_TIMEOUT,
                                    verify=GC.VERIFY_CERTIFICATE)
        return response
