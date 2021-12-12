from settings import BASE_URL, METHOD, data_set_name, api_key
from cached_property import cached_property
import requests    
from .meta import Meta

class BEA:
    def __init__(self):
        self.url = BASE_URL
        self.dataset = None

    def show_dataset_tables(self):
        if self.dataset is None:
            return 'Method Not Allowed with this Dataset'
        endpoint = self.url + f'&METHOD={METHOD["parameter_values"]}' + f'&DATASETNAME={self.dataset}'+ f'&ParameterName={"TableID"}'
        response = requests.get(endpoint)
        try:
            resp = response.json()['BEAAPI']['Results']['ParamValue']
        except:
            endpoint = self.url + f'&METHOD={METHOD["parameter_values"]}' + f'&DATASETNAME={self.dataset}'+ f'&ParameterName={"TableName"}'
            response = requests.get(endpoint)  
            resp = response.json()['BEAAPI']['Results']['ParamValue']       
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
    
    @cached_property
    def api_dataset_meta_data(self):
        api_dataset_meta_data = APIDatasetMetaData()
        return api_dataset_meta_data
    
    ################### Cached Properties #######################

class NIPA(BEA):
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
    def __init__(self):
        super().__init__()
        self.dataset = 'NIPA'

    def access_table_data(self, table_id, freq='A', year=2020):
        endpoint = (self.url
        + f'&METHOD={METHOD["get_data"]}'
        + f'&DATASETNAME={self.dataset}'+ f'&TableName={table_id}'
        + f'&year={year}'
        + f'&frequency={freq}')
        response = requests.get(endpoint)
        resp = response.json()['BEAAPI']['Results']['Data']
        return resp

class NIUnderlyingDetail(BEA):
    '''
    some crap
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'NIUnderlyingDetail'

class InputOutput(BEA):
    '''
    some crap
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

class IIP(BEA):
    '''
    issue with table method
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'IIP'

class MNE(BEA):
    '''
    issue with table method
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'MNE'

class IntlServTrade(BEA):
    '''
    issue with table method
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'IntlServTrade'



class APIDatasetMetaData(BEA):
    '''
    issue with table method
    '''
    def __init__(self):
        super().__init__()
        self.dataset = 'APIDatasetMetaData'