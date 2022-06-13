import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import geopandas as gpd
from plotly.graph_objs import Scatter, Figure, Layout
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import folium
import csv

with st.echo(code_location='below'):
  st.write("hello")
  
  @st.cache
  
  def get_data(data_url): 
     return (
         pd.read_csv(data_url)
         .assign(
             harvest_year=lambda x: pd.to_datetime(
                 x["Harvest.Year"], format="%Y", errors='coerce'
                 )
          )
      ).drop("Harvest.Year", 1) 
  
  url = (
        "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
  )
  state_geo = f"{url}/us-states.json"
  df_startups = pd.read_csv("https://github.com/Kitiara2/repo/raw/main/startup%20data.csv")
  
  df_startups_total = df_startups.groupby("state_code").sum().reset_index()
  df_startups_total
  
  m = folium.Map(location=[48, -102], zoom_start=1)

  
  folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=df_startups_total,
    columns=["state_code", "funding_total_usd"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",
  ).add_to(m)


  folium.LayerControl().add_to(m)
  st_data = st_folium(m, width = 725)
  st_data
