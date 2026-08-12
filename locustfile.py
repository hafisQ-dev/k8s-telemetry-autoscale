from locust import HttpUser, between, task

class TelemetryUser(HttpUser):
    wait_time = between(1, 2)

    # Fonksiyon adı: trafo_verisi_gonder (Anlamlı herhangi bir isim)
    @task
    def trafo_verisi_gonder(self):
        # Gerçek iş yükü: Telemetri endpoint'ine POST isteği atar
        payload = {
            "voltage": 220,
            "current": 15,
            "temperature": 45
        }
        self.client.post("/telemetry", json=payload)
