from locust import HttpUser, task, between
import json
import random

class Chi2User(HttpUser):
    """Load test for pure-Python and SciPy chi-square endpoints"""
    wait_time = between(1, 3)

    @task
    def chi2_pure(self):
        """Test pure-Python chi-square endpoint"""
        num_items = random.randint(1, 20)
        payload = []
        for _ in range(num_items):
            x = random.uniform(0, 20)
            df = random.uniform(0.1, 10)
            lower_tail = random.choice([True, False])
            payload.append({"x": x, "df": df, "lower_tail": lower_tail})
        headers = {"Content-Type": "application/json"}
        self.client.post("/chi2_probabilities", data=json.dumps(payload), headers=headers)

    @task
    def chi2_scipy(self):
        """Test SciPy-based chi-square endpoint"""
        num_items = random.randint(1, 20)
        payload = []
        for _ in range(num_items):
            x = random.uniform(0, 20)
            df = random.uniform(0.1, 10)
            lower_tail = random.choice([True, False])
            payload.append({"x": x, "df": df, "lower_tail": lower_tail})
        headers = {"Content-Type": "application/json"}
        self.client.post("/chi2_scipy", data=json.dumps(payload), headers=headers) 