from settings import BASE_URL, METHOD, api_key
import requests

class BEA:
    def __init__(self):
        self.url = BASE_URL
        self.meta = self.Meta(self.url)

    class Meta():
        def __init__(self, url):
            self.url = url
            super().__init__()

        def get_available_data_sets(self):
            self.url += f'&METHOD={METHOD["datasets"]}'
            print(self.url)
            response = requests.get(self.url)
            resp = response.json()
            return resp