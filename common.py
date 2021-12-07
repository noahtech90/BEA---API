import pandas as pd
import requests
from pprint import pprint
from urllib.request import urlopen
import plotly.graph_objects as go
from settings import *
import json
import plotly.express as px

def generate_df(**kwargs):

    pass

def clean_data(df):
    df['DataValue'] = df['DataValue'].apply(lambda x: x.replace(",",""))
    df['DataValue'] = df['DataValue'].apply(lambda x: x.replace("(NA)", "0"))
    df['DataValue'] = df['DataValue'].astype('float')
    return df

######################################################
################ Visuals ############################
###################################################

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

def private_investment_us(bea):
    columns = pd.DataFrame(bea.nipa.access_table_data(
        table_id='T50203', 
        freq='A', 
        year=1995)).columns


    gross_domestic_investment =  pd.DataFrame(columns=columns)
    year_range = range(1940, 2020)

    for year in year_range:
        df = pd.DataFrame(bea.nipa.access_table_data(
            table_id='T50203', 
            freq='A', 
            year=year)).iloc[0]
        gross_domestic_investment = gross_domestic_investment.append(df)
    gross_domestic_investment = clean_data(gross_domestic_investment)
    gross_domestic_investment = gross_domestic_investment.rename(columns={'DataValue': 'Investment', 'TimePeriod': 'Year'})
    gross_domestic_investment.plot.line(x='Year', y='Investment')
