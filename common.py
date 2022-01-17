
import pandas as pd
from pprint import pprint
from urllib.request import urlopen
import plotly.graph_objects as go
from settings import *
import json
import plotly.express as px
from re import sub

def time_frame(range_num = 10):
    '''
    generates range of numbers ending in current year
    '''
    year_range = range(CURRENT_YEAR - range_num, CURRENT_YEAR)
    return year_range

def clean_data(df):
    df['DataValue'] = df['DataValue'].apply(lambda x: x.replace(",",""))
    df['DataValue'] = df['DataValue'].apply(lambda x: x.replace("(NA)", "0"))
    df['DataValue'] = df['DataValue'].astype('float')
    return df

def access_table_by_year(db_object, table_id, years, freq='A', iloc=0):
    '''
    access data over period of times
    '''
    years = time_frame(years)
    df_cols = pd.DataFrame(db_object.access_table(table_id)).columns
    df = pd.DataFrame(columns=df_cols)
    for year in years:
        year_df = pd.DataFrame(db_object.access_table(table_id, year=year, freq=freq)).iloc[iloc]
        df = df.append(year_df)
    df = clean_data(df)
    return df

################ Visuals ############################

def county_chloropleth(df):
    '''
    creates chloropleth mapping for county data

    color scale determined by min and max values available
    '''
    df = clean_data(df)
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    
    min_value = df['DataValue'].min()
    max_value = df['DataValue'].max()

    fig = px.choropleth(df, geojson=counties, locations='GeoFips', color='DataValue',
                            color_continuous_scale="spectral_r",
                            range_color=(min_value, max_value),
                            scope="usa",
                            )
    fig.update_layout(
        geo_scope='usa', # limit map scope to USA
        margin={"r":0,"t":0,"l":0,"b":0}
        )
    return fig

def state_choropleth(df):
    '''
    clean choropleth data and return graph
    '''
    # filter down to first quarter if data split quarterly
    #if 'TimePeriod' in df.columns:
        #df = df[df['TimePeriod'].str[-2:] == 'Q1']
        #df = df[df['TimePeriod'].str[-2:] == 'Q1']
        #df['TimePeriod'] = df['TimePeriod'].str[:-2]
    
    if len(df) == 60:
        df = clean_data(df)
        df = df[1:-8]
    
    # Map State Names to Short Hand Code
    df['Code'] = df['GeoName'].map(code)
    
    # Generate Figure
    fig = px.choropleth(df,
                        locations='Code',
                        color='DataValue',
                        color_continuous_scale='spectral_r',
                        hover_name='Code',
                        locationmode='USA-states',
                        labels={'Income By State'},
                        scope='usa')
    
    return fig

############################## Utility #################
def convert_snake_case(s):
    '''
    convert given string to snake case syntax

    TODO: This is not workiing splitting string like "gdp" to g_d_p
    '''
    return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()

def convert_dataset_to_method(df):
    '''
    takes in dataset name response and converts to method
    '''
    df['DatasetName'] = df['DatasetName'].apply(lambda x: convert_snake_case(x))
    df['DatasetName'] = df['DatasetName'].str.replace('gd_p', 'gdp_')
    return df

def to_df(data):
    '''
    convert to dataframe
    '''
    return pd.DataFrame(data)

def dict_to_url(endpoint_dict: dict) -> str:
    '''
    convert endpoint dictionary to url used to query api
    '''
    endpoint = str(endpoint_dict).replace(':', '=').replace('{', '').replace('}', '').replace("'", '').replace(',', '').replace(' ', '')
    keys = endpoint_dict.keys()
    for key in keys:
        position = endpoint.find(key)
        beg = endpoint[:position]
        end = endpoint[position:]
        endpoint = beg + '&' + end
    
    # Above Adds Unncesary & to first Method
    endpoint = endpoint[1:]
    return endpoint
