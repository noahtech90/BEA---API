from settings import BASE_URL, CURRENT_YEAR, METHOD, data_set_name, api_key
from cached_property import cached_property 
import pandas as pd
import requests
from urllib.request import urlopen
import plotly.graph_objects as go
from settings import *
import json
import plotly.express as px

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

    def income_per_capita(df, year):
        '''
        County view of income per capita in the US

        data available starting around 1990???
        '''
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)

        def clean_data(df):
            df['DataValue'] = df['DataValue'].apply(lambda x: x.replace(",",""))
            df['DataValue'] = df['DataValue'].apply(lambda x: x.replace("(NA)", "0"))
            df['DataValue'] = df['DataValue'].astype('int')
            df['DataValue'] = df['DataValue'].apply(lambda x: x * (1.0232)**(2020 - int(year))) 
            return df

        df = clean_data(df)

        fig = px.choropleth(df, geojson=counties, locations='GeoFips', color='DataValue',
                                color_continuous_scale="greens",
                                range_color=(0, 100000),
                                scope="usa",
                                labels={'inc':'income per capital'},
                                title='US Income Per Capita By County'
                                )
        fig.update_layout(
            geo_scope='usa', # limite map scope to USA
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        fig.show()

class NIUnderlyingDetail(BEA):
    '''
    some crap
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
    some crap
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'GDPbyIndustry'

class UnderlyingGDPbyIndustry(BEA):
    '''
    some crap
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'UnderlyingGDPbyIndustry'

class Regional(BEA):
    '''
    issue with table method
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'Regional'

    def access_table(self, table_id, freq='A', year=2020, geo_fips='county', line_code=20):
        '''
        acessing table data for given dataset
        '''
        endpoint = (self.url
        + f'&METHOD={METHOD["get_data"]}'
        + f'&DATASETNAME={self.dataset}'
        + f'&TableName={table_id}'
        + f'&GeoFips={geo_fips}'
        + f'&LineCode={line_code}'
        + f'&year={year}'
        + f'&frequency={freq}')
        response = requests.get(endpoint)
        try:
            return response.json()['BEAAPI']['Results']['Data']
        except:
            return response

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