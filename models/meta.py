from settings import METHOD
import requests    
from .base import BEA

class Meta(BEA):
    '''
    Used for obtaining meta data on all BEA Data tables
    '''
    def __init__(self):
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