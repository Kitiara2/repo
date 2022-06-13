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

  
  def print_hello(name):                                                         
       st.write(f"### Hello, {name}!")
        
  name = st.text_input("Your name", key="name", value="Anonymous")
  print_hello(name)
    
  """
  # Приступим
  В этом проекте я анализирую различные данные по стартапам - их распространение, концентрацию и сферы. В конце мы даже попробуем предсказать, какую сумму инвестиций вы смогли бы получить на вашу идею.
  """
  """
  Как известно, США - родина стартапов, поэтому наиболее точную статистику собирают именно там. С ней и будем работать.
  """
  

  
  url = (
        "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
  )
  state_geo = f"{url}/us-states.json"
  df_startups = pd.read_csv("https://github.com/Kitiara2/repo/raw/main/startup%20data.csv")
  df_startups
  
  """
  # Немного контурных карт
  С помощью библиотеки `folium` нарисуем и покрасим карту США в зависимости от того, сколько инвестиций поднимали стартапы в разных штатах.
  """
  
  df_startups_total = df_startups.groupby("state_code").sum().reset_index()
  df_startups_avarage = df_startups.groupby("state_code").mean().reset_index()

  
  value = st.selectbox(
        "Value", ["Total", "Avarage"]
    )
  
  startups_data= df_startups_total if value == "Total" else df_startups_avarage
  
  m = folium.Map(location=[48, -102], zoom_start=3)

  
  folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=startups_data,
    columns=["state_code", "funding_total_usd"],
    key_on="feature.id",
    fill_color="YlGn" if value == 'Total' else "PuOr",
    fill_opacity=0.7,
    nan_fill_opacity = 0,
    line_opacity=0.2,
    legend_name="Total Founding ($)",
  ).add_to(m)


  folium.LayerControl().add_to(m)
  st_data = st_folium(m, width = 725)
  st_data
  
  """
  P.S.: Если присмотреться, можно заметить, что в некоторых штатах среднее количество инвестиций гораздо выше по шкале, чем общее. Будем считать, что там живут гении, запускающие стартапы-единороги.
  """
  
  """
  # Что по сферам
  Логично предположить, что уровень капитализации стартапа зависит от сферы, к которой он принадлежит. Было бы интересно посмотреть, что сейчас в тренде. К сожалению, в изначальных данных у нас нет удобного столбца для построения графика, данные по сферам представлены в булевом формате. 
  """
  
  """
  Давайте считать, что это шанс продемонстрировать умение работать с `pandas`
  """
  
  df_startups['industry_type'] = df_startups['is_software']*1 + df_startups['is_web']*2 + df_startups['is_mobile']*3 + df_startups['is_enterprise']*4 + df_startups['is_advertising']*5 + df_startups['is_gamesvideo']*6 + df_startups['is_ecommerce']*7 + df_startups['is_biotech']*8 +df_startups['is_consulting']*8 + df_startups['is_othercategory']*9
  
  df_startups
