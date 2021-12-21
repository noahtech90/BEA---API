
import pandas as pd
from pprint import pprint
from urllib.request import urlopen
import plotly.graph_objects as go
from settings import *
import json
import plotly.express as px
import re

def time_frame(range_num = 10):
    '''
    function to return range of numbers for 
    '''
    year_range = range(CURRENT_YEAR - range_num, CURRENT_YEAR)
    return year_range

def clean_data(df):
    df['DataValue'] = df['DataValue'].apply(lambda x: x.replace(",",""))
    df['DataValue'] = df['DataValue'].apply(lambda x: x.replace("(NA)", "0"))
    df['DataValue'] = df['DataValue'].astype('float')
    return df

def time_frame_data(db_object, table_id, years, freq='A', iloc=0):
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

def private_investment_us(bea):
    columns = pd.DataFrame(bea.nipa.access_table_data(
        table_id='T50203', 
        freq='A', 
        year=1995)).columns


    gross_domestic_investment =  pd.DataFrame(columns=columns)
    year_range = time_frame()

    for year in year_range:
        df = pd.DataFrame(bea.nipa.access_table_data(
            table_id='T50203', 
            freq='A', 
            year=year)).iloc[0]
        gross_domestic_investment = gross_domestic_investment.append(df)
    gross_domestic_investment = clean_data(gross_domestic_investment)
    gross_domestic_investment = gross_domestic_investment.rename(columns={'DataValue': 'Investment', 'TimePeriod': 'Year'})
    gross_domestic_investment.plot.line(x='Year', y='Investment')

def county_chloropleth(df):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    fig = px.choropleth(df, geojson=counties, locations='GeoFips', color='DataValue',
                            color_continuous_scale="greens",
                            range_color=(0, 130000),
                            scope="usa",
                            )
    fig.update_layout(
        geo_scope='usa', # limit map scope to USA
        margin={"r":0,"t":0,"l":0,"b":0}
        )
    fig.show()

def state_choropleth(df):
    '''
    clean choropleth data and return graph
    '''
    # filter down to first quarter if data split quarterly
    df = df[df['TimePeriod'].str[-2:] == 'Q1']
    if len(df) > 0:
        df = df[df['TimePeriod'].str[-2:] == 'Q1']
        df['TimePeriod'] = df['TimePeriod'].str[:-2]
        df = clean_data(df)
        df = df[1:-8]
    
    # Map State Names to Short Hand Code
    df['Code'] = df['GeoName'].map(code)
    fig = px.choropleth(df,
                        locations='Code',
                        color='DataValue',
                        color_continuous_scale='spectral_r',
                        hover_name='Code',
                        locationmode='USA-states',
                        labels={'Income By State'},
                        scope='usa')
    
    fig.show()

############################## Utility #################
def convert_snake_case(string):
    '''
    convert given string to snake case syntax

    TODO: This is not workiing splitting string like "gdp" to g_d_p
    '''
    string = re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
    return string

def to_df(data):
    '''
    convert to dataframe
    '''
    return pd.DataFrame(data)