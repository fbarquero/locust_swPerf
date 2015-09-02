
import requests
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Transaction(object):

    def run(self):
        session = requests.Session()
        session.get("http://www.example.com")
        session.close()



if __name__ == '__main__':
    trans = Transaction()
    trans.run()
