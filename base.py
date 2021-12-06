from settings import BASE_URL, METHOD, data_set_name, api_key
import requests


class BEA:
    def __init__(self):
        self.url = BASE_URL
        self.dataset = None
        self.meta = self.Meta(self.url)
        self.nipa = self.NIPA(self.url)
    
    def show_dataset_tables(self):
        if self.dataset is None:
            return 'Method Not Allowed with this Dataset'
        endpoint = self.url + f'&METHOD={METHOD["parameter_values"]}' + f'&DATASETNAME={self.dataset}'+ f'&ParameterName={"TableID"}'
        response = requests.get(endpoint)
        resp = response.json()
        return resp

    class Meta():
        '''
        Used for obtaining meta data on all BEA Data tables
        '''
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
        
    class NIPA:
        '''
        GDP, Income, and Saving tables

        Gross domestic product (GDP)
        Gross domestic income (GDI)
        National income
        Corporate profits
        Government receipts and expenditures
        Personal income and disposable personal income
        Personal consumption expenditures (PCE), or consumer spending
        Personal saving

        T50203 - saving and investment by sector
        '''
        def __init__(self, url):
            self.url = url
            self.dataset = 'NIPA'
            super().__init__()

        def access_table_data(self, table_id, freq, year):
            endpoint = (self.url
            + f'&METHOD={METHOD["get_data"]}'
            + f'&DATASETNAME={self.dataset}'+ f'&TableName={table_id}'
            + f'&year={year}'
            + f'&frequency={freq}')
            response = requests.get(endpoint)
            resp = response.json()['BEAAPI']['Results']['Data']
            return resp
        

        