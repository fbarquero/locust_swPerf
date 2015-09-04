from requests import Session

session = Session()
r = session.get("http://localhost:8089")
print r.content
