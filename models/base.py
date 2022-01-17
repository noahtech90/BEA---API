from settings import BASE_URL, CURRENT_YEAR, METHOD, data_set_name, api_key
from cached_property import cached_property 
import pandas as pd
import requests
from urllib.request import urlopen
import plotly.graph_objects as go
from settings import *
import json
import plotly.express as px
from common import dict_to_url

class BEA:
    '''
    base class all datasets inherit from
    '''
    def __init__(self):
        self.url = BASE_URL
        self.dataset = None

    def access_table(self, table_id, freq='A', year=2020):
        '''
        acessing table data for given dataset
        '''
        endpoint = (self.url
        + f'&METHOD={METHOD["get_data"]}'
        + f'&DATASETNAME={self.dataset}'+ f'&TableName={table_id}'
        + f'&year={year}'
        + f'&frequency={freq}')
        response = requests.get(endpoint)
        try:
            return response.json()['BEAAPI']['Results']['Data']
        except:
            return response

    def show_tables(self):
        '''
        show list of tables tied to given datasaet
        '''
        if self.dataset is None:
            return 'Method Not Allowed with this Dataset'
        endpoint = self.url + f'&METHOD={METHOD["parameter_values"]}' + f'&DATASETNAME={self.dataset}'+ f'&ParameterName={"TableID"}'
        response = requests.get(endpoint)
        try:
            resp = response.json()['BEAAPI']['Results']['ParamValue']
        except:
            endpoint = self.url + f'&METHOD={METHOD["parameter_values"]}' + f'&DATASETNAME={self.dataset}'+ f'&ParameterName={"TableName"}'
            response = requests.get(endpoint)  
            try:
                resp = response.json()['BEAAPI']['Results']['ParamValue'] 
            except:
                resp = response
        return resp

    def get_available_parameters(self):
        endpoint = self.url + f'&METHOD={METHOD["parameter_list"]}' + f'&DATASETNAME={self.dataset}'
        response = requests.get(endpoint)
        resp = response.json()
        return resp
    
    def get_parameter_values(self, table_id, parameter_name):
        endpoint = (self.url 
        + f'&METHOD={METHOD["parameter_value_filt"]}' 
        + f'&TableName={table_id}' 
        + f'&DATASETNAME={self.dataset}'
        + f'&TargetParameter={parameter_name}')
        response = requests.get(endpoint)
        resp = response.json()['BEAAPI']['Results']
        return resp

    ################### Cached Properties #######################
    @cached_property
    def nipa(self):
        nipa = NIPA()
        return nipa
    
    @cached_property
    def meta(self):
        meta = Meta()
        return meta
    
    @cached_property
    def ni_underlying_detail(self):
        ni_underlying_detail = NIUnderlyingDetail()
        return ni_underlying_detail
    
    @cached_property
    def mne(self):
        mne = MNE()
        return mne
    
    @cached_property
    def fixed_assets(self):
        fixed_assets = FixedAssets()
        return fixed_assets
    
    @cached_property
    def ita(self):
        ita = ITA()
        return ita
    
    @cached_property
    def iip(self):
        iip = IIP()
        return iip
    
    @cached_property
    def input_output(self):
        input_output = InputOutput()
        return input_output
    
    @cached_property
    def intl_serv_trade(self):
        intl_serv_trade = IntlServTrade()
        return intl_serv_trade
    
    @cached_property
    def gdp_by_industry(self):
        gdp_by_industry = GDPbyIndustry()
        return gdp_by_industry
    
    @cached_property
    def regional(self):
        regional = Regional()
        return regional
    
    @cached_property
    def underlying_gdp_by_industry(self):
        underlying_gdp_by_industry = UnderlyingGDPbyIndustry()
        return underlying_gdp_by_industry
    
    ################### Cached Properties #######################

class NIPA(BEA):
    '''
    GDP, Income, and Saving tables

    T50203 - saving and investment by sector
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'NIPA'

class NIUnderlyingDetail(BEA):
    '''
    not sure
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'NIUnderlyingDetail'

class InputOutput(BEA):
    '''
    Commodity tables detailing comodities listed by industry
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'InputOutput'

class GDPbyIndustry(BEA):
    '''
    GDP by Industry data
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'GDPbyIndustry'

class UnderlyingGDPbyIndustry(BEA):
    '''
    not sure
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'UnderlyingGDPbyIndustry'

class Regional(BEA):
    '''
    Regional data on various economic stats in US
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'Regional'

    def access_table(self, table_id, freq='A', year=2020, geo_fips='county', line_code=20):
        '''
        acessing table data for given dataset
        '''
        endpoint = {
            'METHOD': METHOD["get_data"],
            'DATASETNAME': self.dataset,
            'TableName': table_id,
            'GeoFips': geo_fips,
            'LineCode': line_code,
            'year': year,
            'frequency': freq
        }
        url = (self.url + dict_to_url(endpoint))
        response = requests.get(url)
        try:
            return response.json()['BEAAPI']['Results']['Data']
        except:
            if response.status_code == 200 and 'Error' in response.json()['BEAAPI'].keys():
                # will need to make this more versatile but for now just querying for line code
                line_code = self.get_parameter_values(table_id, 'LineCode')['ParamValue'][0]['Key']
                endpoint['LineCode'] = line_code
                url = (self.url + dict_to_url(endpoint))
                
                response = requests.get(url)
                try:
                    return response.json()['BEAAPI']['Results']['Data']
                except:
                    endpoint['GeoFips'] = 'State'
                    url = (self.url + dict_to_url(endpoint))
                    response = requests.get(url)
                    try:
                        return response.json()['BEAAPI']['Results']['Data']
                    except: 
                        return response.json()

class FixedAssets(BEA):
    '''
    issue with table method
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'FixedAssets'

class ITA(BEA):
    '''
    issue with table method
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'ITA'

    def show_tables(self):
        '''
        show list of tables tied to given datasaet
        '''
        return pd.DataFrame([{'table': 'One Table Available'}])

class IIP(BEA):
    '''
    issue with table method
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'IIP'

    def show_tables(self):
        '''
        show list of tables tied to given datasaet
        '''
        return pd.DataFrame([{'table': 'One Table Available'}])

class MNE(BEA):
    '''
    issue with table method
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'MNE'

    def show_tables(self):
        '''
        show list of tables tied to given datasaet
        '''
        return pd.DataFrame([{'table': 'One Table Available'}])

class IntlServTrade(BEA):
    '''
    issue with table method
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'IntlServTrade'

    def show_tables(self):
        '''
        show list of tables tied to given datasaet
        '''
        if self.dataset is None:
            return 'Method Not Allowed with this Dataset'
        endpoint = self.url + f'&METHOD={METHOD["parameter_values"]}' + f'&DATASETNAME={self.dataset}'+ f'&ParameterName={"TypeOfService"}'
        response = requests.get(endpoint)
        try:
            resp = response.json()['BEAAPI']['Results']['ParamValue']
        except:
            resp = response
        return resp

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