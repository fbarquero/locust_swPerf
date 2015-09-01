__author__ = 'alonsobarquero'

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sw_requests.sowatest import SowatestRequests

print("Running sowatest hits without proxy...\n")

class Transaction(object):
    def run(self):
        try:
            sowatest = SowatestRequests()
            response = sowatest.sowatest_no_proxy()
            assert response.status_code is 200, "unexpected response status code {}".format(response.status_code)
            assert 'id="facebook"' in response.content
        except Exception, e:
            raise
        finally:
            sowatest.session.close()


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
