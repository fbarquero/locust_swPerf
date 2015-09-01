# __author__ = 'alonsobarquero'
# import requests
#
# HEADERS = {
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/43.0.2357.134 Safari/537.36',
#         'Accept-Encoding': 'gzip, deflate'
#
#     }
#
#
# session = requests.Session()
# response = session.get("https://google.com", headers=HEADERS)
#
#
# payload = {"content":[{"nombre": "Francisco", "apellido": "Barquero"},
#                       {"nombre": "Francisco", "apellido": "Barquero"},
#                       {"nombre": "Francisco", "apellido": "Barquero"}]
#            }
# response_post = session.post("localhost:8000/proyecto/api/algo,json", data=payload, headers=HEADERS)
#
# print response.text

import requests
import json

s = requests.Session()
payload = {'content': [{"nombre": "Jonathan", "datos": "Estudiante bootcamp"},
                       {"nombre": "Gabriel", "datos": "Estudiante tambien"},
                       {"nombre": "Ronnald", "datos": "Es buena guila ... he knows ... how to ..."}]}
p = json.dumps(payload)
print p
p2 = str(payload)
print p2


HEADERS = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/44.0.2403.89 Safari/537.36",
    'Content-type': 'application/json',
    'Accept': 'application/json',

}
r = s.post("http://127.0.0.1:8000/test_bootcamp/servicio/api.json", headers=HEADERS, data=p)
print r.content
print r.status_code
