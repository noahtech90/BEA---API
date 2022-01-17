
import streamlit as st
import pandas as pd
from common import  generate_visualization, time_frame,  to_df, convert_dataset_to_method
import plotly.graph_objects as go
from settings import *
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
    table_name = st.selectbox('Select Table', tables['Desc'])
    if dataset_name == 'regional':
        table_id = tables[tables['Desc'] == table_name]['Key'].iloc[0]
        st.header(table_name) 
    if not table_name is None:
        # Show Years tied to data
        year_df = to_df(class_.get_parameter_values(table_id, 'year')['ParamValue'])
        year = st.selectbox('Year to Access Data', year_df)
        try:
            df = pd.DataFrame(class_.access_table(table_id=table_id, year=year))
            st.write(df)
            visual = st.checkbox('Visualize Data')
            st.subheader(table_name) 
            if visual:
                try:
                    st.plotly_chart(generate_visualization(df))
                except:
                    st.error('Issue Visualizing Data')
        except: 
            st.error(class_.access_table(table_id=table_id, year=year))

