__author__ = 'alonsobarquero'
# from lxml import html
from BeautifulSoup import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()

from configs.config import GlobalConfigs as GC, CertificateConfigs as CRT, ProxyConfigs as PC
from sw_request_core import request as sw_r


class Login:

    def __init__(self):
        self.session = None


    def sw_valid_login(self, username, password, url):
        """
        Authenticate a valid user through the proxy to access a Social Networking Website
        IMPORTANT: NO NOT RUN THOSE PERFORMANCE TESTS AGAINST AN OFFICIAL SOCIAL NETWORKING WEBSITE
        YOUR IP MY BE BLACK LISTED.
        :param username: Valid Username
        :param password: Valid Password
        :param url: Valid Social Networking Website i.e: https://www.facebook.com
        :return: response object, with the Social Networking Website Login homepage.
        """
        # Creates session
        self.session = requests.Session()
        # Set Certificate to authenticate in the proxy server and socialware sites
        self.session.cert = (CRT.CERT_CRT_PATH, CRT.CERT_KEY_PATH)
        # Accessing the Social Networking Website
        response = sw_r.get_with_proxy(self.session, url) #s.get(url, allow_redirects=False, headers=GC.HEADERS, proxies=GC.proxies)
        # Loggin in IDP and get the response to redirect to the Social Networking  Website
        response = self.authenticate_in_idp(username, password)
        # Continue the redirect to the Social Networking Website
        response = sw_r.get_with_proxy(self.session, response.headers['location'])
        return response


    def authenticate_in_idp(self ,username, password):
        """
        Authenticate a valid Socialware through SAML2.0 when tries to access a Social Networking Site through the proxy
        :param username: Valid Socialware user
        :param password: Valid Socialware password for the user specified
        :return: response object, to redirect the user to the Social Networking site specified.
        """
        # Form data to to log into IDP
        form_data = {'j_username': username,
                     'j_password': password,
                     'submit.x':72,
                     'submit.y':23,
                     'submit':'LOGIN'
                     }
        # POST to start the Authentication process at IDP
        response = self.session.post("https://app.qa1.socialware.com/idp/Authn/UserPassword", form_data, allow_redirects=False, headers=GC.HEADERS, timeout=GC.GLOBAL_REQUEST_TIMEOUT, verify=GC.VERIFY_CERTIFICATE)
        # Get the SAML2 Token
        response = self.session.get(response.headers['location'], allow_redirects=False, headers=GC.HEADERS, timeout=GC.GLOBAL_REQUEST_TIMEOUT, verify=GC.VERIFY_CERTIFICATE)
        #Parse the HTML Response, obtain the SAML Token and set the payload to send back the SAML Token
        soup = BeautifulSoup(response.text)
        saml_token = soup.find("input", {"name": "SAMLResponse"})
        form_data = {
            'SAMLResponse': saml_token["value"]
        }

        # tree = html.fromstring(str(response.text))
        # form_data = {
        #     'SAMLResponse': tree.xpath("//input[@name='SAMLResponse']/@value")
        # }
        #POST to send the SAML2 Token and catch up back the flow to Facebook
        response = self.session.post("https://session.socialware.com/saml/acs", form_data, allow_redirects=False, headers=GC.HEADERS, proxies=PC.PROXIES, timeout=GC.GLOBAL_REQUEST_TIMEOUT, verify=GC.VERIFY_CERTIFICATE)
        return response
