
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
datasets_df = pd.DataFrame(bea.meta.get_available_data_sets()['BEAAPI']['Results']['Dataset'])
datasets_df = convert_dataset_to_method(datasets_df)

st.header("Stream Lit Display of BEA Website")

dataset_name = st.selectbox('Choose Dataset', datasets_df)
if not dataset_name is None:
    class_ = getattr(bea, dataset_name)
    tables = class_.show_tables()
    table_name = st.selectbox('Select Tabele', to_df(tables))
