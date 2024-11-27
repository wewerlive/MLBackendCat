from locust import HttpUser, task, between
import json

reqObj = json.loads(open("./sampleRequest.json").read())

class PerformanceTests(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_tf_predict(self):
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        res = self.client.post("/tryon",
                               data=json.dumps(reqObj),
                               headers=headers)
        print("res", res.json())