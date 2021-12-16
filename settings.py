import os
import pandas as pd

api_key = os.environ.get('bea_key', None)
CURRENT_YEAR = 2020
BASE_URL = f'https://apps.bea.gov/api/data?'+ f'&USERID={api_key}'

METHOD = {'none': None, 
        'get_data': 'GETDATA', 
        'parameter_value_filt': 'GetParameterValuesFiltered', 
        'parameter_values': 'GETPARAMETERVALUES', 
        'datasets': 'GETDATASETLIST', 
        'parameter_list': 'getparameterlist'
        }
data_set_name = {
    'none': None,
    'regional': 'Regional',
    'gdp_by_industry': 'GDPbyIndustry',
    'input_output': 'InputOutput'
}
table_name = [None, 'CAINC4', 'IIP']
geo_fips = {'none': None, 'county': 'County', 'state': 'State'}
frequency = {'none': None, 'monthly': 'M', 'yearly': 'Y'}
line_code = [None, '30']
parameter_name = [None, 'Frequency', 'Year', 'Industry', 'TableId', 'TableName']
target_parameter = [None, 'LINECODE&TABLENAME', 'TableName']
result_format = [None,'JSON']


'''
base_url = (f'https://apps.bea.gov/api/data?'
+ f'&USERID={api_key}'
+ f'&METHOD={method["parameter_values"]}'
+ f'&DATASETNAME={data_set_name["regional"]}'
+ f'&GeoFips={geo_fips["state"]}'
+ f'&year=2010'
+ f'&frequency={frequency["none"]}'
+ f'&LINECODE={line_code[0]}'
+ f'&TableName={table_name[0]}'
+ f'&TargetParameter={target_parameter[0]}'
+ f'&ResultFormat={result_format[1]}'
+ f'&ParameterName={parameter_name[5]}')

'''