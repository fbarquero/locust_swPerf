import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from BeautifulSoup import BeautifulSoup

from sw_requests.login import Login
from configs.config import GlobalConfigs as GC
from utilities import sw_user_management as usrs

users_pool = usrs.get_user_pool()


class Transaction(object):
#TODO: measure the time that the page we did hit takes to render in a real browser
#TODO: add the 3 different scenarios, login once, login every time, login expires.
#TODO: add flag for 1 user concurently executed * amount of threads "use_one_user_concurrent = on" in config file
    def run(self):
        try:
            user_credentials = users_pool.pop(0)
            self.user_login = Login()
            # print("User: {}".format(user_credentials))
            r = self.user_login.sw_valid_login(username=user_credentials, password=user_credentials, url=GC.SOCIAL_NETWORKING_URLs['sowatest'], time_out=15)
            soup = BeautifulSoup(r.text)
            # Assert Section
            assert r.status_code == 200, "unexpected status"
            assert "Access Denied" in str(soup.find("title").text)
            assert '<div id="blockedBanner">' in r.text

        except Exception, e:
            if e.message=='location':
                raise Exception('Possible authentication error against IDP!')
            raise
        finally:
            self.user_login.session.close()
            users_pool.append(user_credentials)


# if __name__ == '__main__':
#     trans = Transaction()
#     trans.run()
