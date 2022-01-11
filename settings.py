import os
import pandas as pd

api_key = os.environ.get('bea_key', None)
CURRENT_YEAR = 2021
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


code = {'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'}

YEARS = range(1970, CURRENT_YEAR)