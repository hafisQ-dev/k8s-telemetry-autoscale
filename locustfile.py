from locust import HttpUser, between, task

class TelemetryUser(HttpUser):
    wait_time = between(1, 2)

    # Function name: send_trafe_data (any meaningful name)
    @task
    def send_trafo_data(self):
        # Real work load: Telemetri endpoint'ine POST isteği atar
        payload = {
            "voltage": 220,
            "current": 15,
            "temperature": 45
        }
        self.client.post("/telemetry", json=payload)
