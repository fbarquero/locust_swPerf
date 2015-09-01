import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sw_requests.download_requests import Download

print("Running Download tests for Proxy pac file.")

class Transaction(object):
    def run(self):
        try:
            download = Download()
            response = download.get_pac_file()
            assert response.status_code is 200, "unexpected response status code"
            assert "function FindProxyForURL(url, host)" in response.content
        except Exception, e:
            raise
        finally:
            download.session.close()


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
