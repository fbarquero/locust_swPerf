__author__ = 'alonsobarquero'

import requests
requests.packages.urllib3.disable_warnings()

from configs.config import ProxyConfigs as PC
from configs.config import GlobalConfigs as GC


class Download():

    def __init__(self):
        self.session = None

    def get_pac_file(self):
        """
        Downloads the Proxy authoconfiguration pac by using a specific user session
        the pack files are downloaded at ../pac_file_downloads folder
        :param user: Username
        :return:
        """
        # Creates a new requests session object
        self.session = requests.Session()
        # Executes request get to the pac file url
        response = self.session.get(PC.PROXY_PAC_URL, timeout=GC.GLOBAL_REQUEST_TIMEOUT)
        # Mimic the download process by returning the response with the pac file content inside response.content
        return response




