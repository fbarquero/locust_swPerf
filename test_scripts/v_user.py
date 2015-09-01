
import requests
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Transaction(object):
    def __init__(self):
        self.count = 0

    def run(self):
        session = requests.Session()
        session.get("http://www.example.com")
        session.close()
        self.count += 1



if __name__ == '__main__':
    trans = Transaction()
    trans.run()
