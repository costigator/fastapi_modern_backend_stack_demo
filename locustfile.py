from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 1.5)
    headers = ""

    def on_start(self):
        response = self.client.post("/login/token", data={"username":"demo", "password":"demo"})
        auth_token = response.json()['access_token']
        self.headers = {"Authorization": f"Bearer {auth_token}"}

    @task
    def list_users(self):
        self.client.get("/users")

    @task
    def get_candlesticks(self):
        self.client.get("/candlesticks")

    @task
    def get_candlesticks_with_redis_cache(self):
        self.client.get("/candlesticks/withrediscache")

    @task
    def get_candlesticks_with_rate_limit(self):
        self.client.get("/candlesticks/withratelimit")

