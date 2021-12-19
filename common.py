from numpy import double
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
