from settings import BASE_URL, METHOD, data_set_name, api_key
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
            endpoint = self.url + f'&METHOD={METHOD["datasets"]}'
            response = requests.get(endpoint)
            resp = response.json()
            return resp
        
        def get_available_parameters(self, dataset):
            endpoint = self.url + f'&METHOD={METHOD["parameter_list"]}' + f'&DATASETNAME={dataset}'
            response = requests.get(endpoint)
            resp = response.json()
            return resp
        
        def get_parameter_values(self, dataset, parameter_name):
            endpoint = self.url + f'&METHOD={METHOD["parameter_values"]}' + f'&DATASETNAME={dataset}'+ f'&ParameterName={parameter_name}'
            response = requests.get(endpoint)
            resp = response.json()
            return resp
        