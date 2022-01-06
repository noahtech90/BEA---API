
import streamlit as st
import pandas as pd
from common import time_frame_data
from common import clean_data, time_frame, time_frame_data, county_chloropleth, state_choropleth, to_df, convert_dataset_to_method
from urllib.request import urlopen
import plotly.graph_objects as go
from settings import *
import plotly.express as px
from models.base import BEA

bea = BEA()

# Show Datasets
datasets_df = pd.DataFrame(bea.meta.get_available_data_sets()['BEAAPI']['Results']['Dataset'])
datasets_df = datasets_df[datasets_df.DatasetName != 'APIDatasetMetaData']
datasets_df = convert_dataset_to_method(datasets_df)

# Header
st.header("Bureau of Economic Analysis - Visualization")

dataset_name = st.selectbox('Choose Dataset', datasets_df)
if not dataset_name is None:
    class_ = getattr(bea, dataset_name)
    tables = to_df(class_.show_tables())
    table_name = st.selectbox('Select Table', tables)
    if dataset_name == 'regional':
        table_desc = tables[tables['Key'] == table_name]
        st.header(table_desc['Desc'].iloc[0])
    
    if not table_name is None:
        try:
            st.write(pd.DataFrame(class_.access_table(table_name)))
        except: 
            st.error('Cannot Access table')
