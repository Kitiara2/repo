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


  countries =("https://github.com/Kitiara2/repo/raw/main/country.csv")
  df_c = pd.read_csv(countries)
  
  investments =("https://github.com/Kitiara2/repo/blob/main/startup%20data.csv")
  df = pd.read_csv("https://github.com/Kitiara2/repo/raw/main/startup%20data.csv")
  
  df

  m = folium.Map(location=[48, -102], zoom_start=1)

