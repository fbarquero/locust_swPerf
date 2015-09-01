import sys
from BeautifulSoup import BeautifulSoup
import os
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sw_requests.sowatest import SowatestRequests
from configs.config import MultiMechanizeConfigs as MM
from custom_runner import custom_runner
from utilities import sw_user_management as usrs

# print("Loading swPerf config info")
# custom_runner.load_swperf_config_data()
# print("Running sowatest login once test...\n")

if MM.USE_PROXY:
    print("Loading user sessions ...\n")
    users_pool = usrs.load_sessions_pickle()
    print("\nUsers loaded successfully\n")


class Transaction(object):
#TODO: measure the time that the page we did hit takes to render in a real browser
#TODO: add the 3 different scenarios, login once, login every time, login expires.
#TODO: add flag for 1 user concurently executed * amount of threads "use_one_user_concurrent = on" in config file
    def run(self):
        try:
            if MM.USE_PROXY:
                user_credentials = users_pool.pop(0)
                proxy_request = SowatestRequests()
                response = proxy_request.sowatest_through_proxy(user_credentials)
                soup = BeautifulSoup(response.text)
                # Assert Section
                assert response.status_code is 200, "unexpected response status code {}".format(response.status_code)
                assert "Access Denied" in str(soup.find("title").text)
                assert '<div id="blockedBanner">' in response.text
            else:
                print("no proxy")
        except Exception, e:
            if MM.USE_PROXY:
                if e.message is 'location':
                    raise Exception('Possible authentication error against IDP!')
            raise
        finally:
            if MM.USE_PROXY:
                users_pool.append(user_credentials)
                proxy_request.session.close()


# For debugging in Pycharm
if __name__ == '__main__':
    trans = Transaction()
    trans.run()
