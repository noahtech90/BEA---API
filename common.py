import pandas as pd
from pprint import pprint
from urllib.request import urlopen
import plotly.graph_objects as go
import json
import plotly.express as px


def generate_df(**kwargs):

    pass

def income_per_capital(year, df):
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
        df['DataValue'] = df['DataValue'].apply(lambda x: x * (1.0232)**(2020 - int(year_setting))) 
        return df

    df = clean_data(df)

    fig = px.choropleth(df, geojson=counties, locations='GeoFips', color='DataValue',
                            color_continuous_scale="Viridis",
                            range_color=(0, 110000),
                            scope="usa",
                            labels={'inc':'income per capital'},
                            title='US Income Per Capita By County'
                            )
    fig.update_layout(
        geo_scope='usa', # limite map scope to USA
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    fig.show()