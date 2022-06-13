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

with st.echo(code_location='below'):
  st.write("hello")
  
#with open('admin_level_9.geojson', encoding = 'utf-8') as f:
#        a = json.load(f)

import csv

with open("investments_VC.csv", encoding='utf-8') as f:
  reader = csv.reader(File)
  for row in reader:
      print(row)

    

