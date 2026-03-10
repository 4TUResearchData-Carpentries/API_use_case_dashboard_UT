import streamlit as st

## Basic elements of the dashboard
st.title("Dataset monitoring dashboard")
st.write("Data from 4TU.ResearchData API")

## Request the data using API
import requests
url="https://data.4tu.nl/v2/articles"

response=requests.get(url)
data=response.json()


## Processing the data

import pandas as pd
df=pd.DataFrame(data)

## Visualizing the data 
st.dataframe(df)