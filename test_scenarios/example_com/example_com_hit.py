from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    def on_start(self):
            pass

    @task(1)
    def index(self):
        self.client.get("/", timeout=10)
98

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 200
    host = "http://www.example.com"
    stop_timeout = 60