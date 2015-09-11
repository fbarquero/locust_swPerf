__author__ = 'alonsobarquero'
import os
import socket


class GlobalConfigs:
    GROUPS_OF = 10
    VERIFY_CERTIFICATE = False
    MAX_OPEN_FILES = 1555653
    GLOBAL_REQUEST_TIMEOUT = 5
    SOCIAL_NETWORKING_URLs = {'sowatest': 'http://www.sowatest.com', 'direct_sowatest': 'http://sowatest.com'}
    DEFAULT_ALIAS_URL = 'https://local.dev.socialware.com:8443/main/saml/SSO/alias/defaultAlias'

    HEADERS = {
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/43.0.2357.134 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate'

    }
    SESSIONS_FILE_NAME = "sessions.obj"
    STARTING_INFO_FILE = "master_pid.obj"
    TMP_FOLDER = "tmp"
    TMP_BASE_PATH = "{}/{}".format(os.path.join(os.path.dirname(__file__), '..'), TMP_FOLDER)
    CHART_JS_PATH = "{}/{}".format(os.path.join(os.path.dirname(__file__), '..'),
                                   "result_analysis/result_report_mockup")
    SESSIONS_FILE_PATH = "{}/{}".format(TMP_BASE_PATH, SESSIONS_FILE_NAME)
    STARTING_INFO_FILE_PATH = "{}/{}".format(TMP_BASE_PATH, STARTING_INFO_FILE)
    MULTI_MECH_DATA_FILE = "multi_mech_data.obj"
    MULTI_MECH_FILE_PATH = "{}/{}".format(TMP_BASE_PATH, MULTI_MECH_DATA_FILE)
    RESULTS_FOLDER = "results"
    RESULTS_BASE_PATH = "{}/{}".format(os.path.join(os.path.dirname(__file__), '..'), RESULTS_FOLDER)


class CertificateConfigs:
    CERTIFICATE_FOLDER = "ssl_certificates"
    CERTIFICATE_NAME = "authority"
    CERT_KEY = "{}.key".format(CERTIFICATE_NAME)
    CERT_CRT = "{}.crt".format(CERTIFICATE_NAME)
    CERT_PEM = "{}.pem".format((CERTIFICATE_NAME))
    CERTIFICATE_BASE_PATH = "{}/{}".format(os.path.join(os.path.dirname(__file__), '..'), CERTIFICATE_FOLDER)
    CERT_KEY_PATH = "{}/{}".format(CERTIFICATE_BASE_PATH, CERT_KEY)
    CERT_CRT_PATH = "{}/{}".format(CERTIFICATE_BASE_PATH, CERT_CRT)
    CERT_PEM_PATH = "{}/{}".format(CERTIFICATE_BASE_PATH, CERT_PEM)


class ProxyConfigs():
    PROXY_PAC_URL = "https://app.qa1.socialware.com/api/pac/3130"
    PROXY_URL = "proxy.qa1.socialware.com"
    PROXIES = {'https': "proxy.qa1.socialware.com:3130", 'http': "proxy.qa1.socialware.com:3130"}
    # PROXY_IP = socket.gethostbyname(PROXY_URL)
    # PROXIES = {'https': "{}:3130".format(PROXY_IP), 'http': "{}:3130".format(PROXY_IP)}
    URLs = ['twitter.com', 'facebook.com', 'linkedin.com', 'sowatest.com', 'proxy.qa1.socialware.com',
            'session.socialware.com']


class LocustConfigs():
    RUN_TIME = 60
    RESULTS_TS_INTERVAL = 5
    RAMPUP = 650
    PROGRESS_BAR = "on"
    CONSOLE_LOGGING = "off"
    XML_REPORT = "on"
    LOGIN_STYLE = "once"
    USERS = 650
    LOCUST_FILE = "hit_sowatest_login_once.py"
    USE_PROXY = True
    CONFIG_FILE_PATH = "{}/config.cfg".format(os.path.join(os.path.dirname(__file__), '..'))
