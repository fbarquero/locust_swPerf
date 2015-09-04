__author__ = 'alonsobarquero'
import urllib2
from configs.config import GlobalConfigs as GC, ProxyConfigs as PC
from utilities import proxy_management as proxy_mngmt


class ProxyRequests:
    def __init__(self, client):
        self.client = client

    def get_with_proxy(self, url, use_proxy_on_first=True):
        proxy = None
        if use_proxy_on_first:
            proxy = PC.PROXIES
        response = self.client.get(url, allow_redirects=False, headers=GC.HEADERS, proxies=proxy,
                                   timeout=GC.GLOBAL_REQUEST_TIMEOUT, verify=GC.VERIFY_CERTIFICATE)
        while response.is_redirect:
            location = response.headers.get('location')
            if location:
                url = urllib2.urlparse.urlparse(location)
                proxy = proxy_mngmt.get_proxy(url.netloc)
                response = self.client.get(location, allow_redirects=False, headers=GC.HEADERS, proxies=proxy,
                                           timeout=GC.GLOBAL_REQUEST_TIMEOUT, verify=GC.VERIFY_CERTIFICATE)
        return response
