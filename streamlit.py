
import streamlit as st
import pandas as pd
from common import  (
                    generate_visualization, 
                    time_frame,  
                    to_df, 
                    convert_dataset_to_method, 
                    normalize_access_table_columns, 
                    generated_year_range_from_df)
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
dataset_desc = st.selectbox('Choose Dataset', datasets_df['DatasetDescription'])
dataset_name = datasets_df[datasets_df['DatasetDescription'] == dataset_desc]['DatasetName'].iloc[0]

if not dataset_name is None:
    class_ = getattr(bea, dataset_name)
    tables = normalize_access_table_columns(to_df(class_.show_tables()))
    tables = normalize_access_table_columns(tables)
    
    try:
        table_name = st.selectbox('Select Table', tables['Desc'])
        # Set Table Key
        table_id = tables[tables['Desc'] == table_name]['Key'].iloc[0]
    except:
        table_name = dataset_desc
        table_id = 1
        #TODO: This is super dumb solution need to think of something better
        # maybe can be some meta data within class that informs path chosen down here
        # 
    st.subheader(table_name) 
    if not table_name is None:
        # Show Years tied to data
        # TODO: Refactor and encapsulate below functionality into function
        try:
            year_df = to_df(class_.get_parameter_values(table_id, 'year')['ParamValue'])
            year = st.selectbox('Year to Access Data', year_df)
        except:
            year_df = to_df(class_.get_parameter_values_nonfiltered(parameter_name='Year')['ParamValue'])
            try:
                year_range = generated_year_range_from_df(year_df, table_id)
                year = st.selectbox('Year to Access Data', year_range)
            except:
                year = st.selectbox('Years to Access Data', year_df)
            
        if table_id != 1:
            df = pd.DataFrame(class_.access_table(table_id=table_id, year=year))
            st.write(df)
            visual = st.checkbox('Visualize Data')

            if visual:
                try:
                    st.markdown(f"{table_name} as of {year}")
                    st.plotly_chart(generate_visualization(df))
                except Exception as e:
                    st.error(e)
        else:
            # Attempting to Access Single Table Datasets
            try:
                df = pd.DataFrame(class_.access_table(year=year))
                st.write(df)
            except:
                st.error("Something went wrong")



