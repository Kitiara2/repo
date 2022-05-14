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
#import webbrowser

with st.echo(code_location='below'):


    def print_hello(name):
        st.write(f"### Hello, {name}!")
        
    name = st.text_input("Your name", key="name", value="Anonymous")
    print_hello(name)
    
    """
    # Приступим
    Кофе - это всегда хорошая идея и топливо для моего существования, поэтому для анализа использован датасет о странах, где добывается кофе. Для начала просто покажу датасет.
    """
    
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


    df_ro = get_data("https://github.com/Kitiara2/repo/raw/main/robusta_data_cleaned.csv")
    df_ro.rename(columns={'Country_of_Origin': 'Country.of.Origin', 'Clean_Cup': 'Clean.Cup'}, inplace=True)
    df_ro['Robusta'] = 1
    df_ro['Arabica'] = 0
    df_ar = get_data("https://github.com/Kitiara2/repo/raw/main/arabica_data_cleaned.csv")
    df_ar['Arabica'] = 1
    df_ar['Robusta'] = 0
    df = pd.concat([df_ar, df_ro], ignore_index=False)
    
    df.rename(columns={'Country.of.Origin': 'Country_of_Origin'}, inplace=True)
    df.rename(columns={'Clean.Cup': 'Clean_Cup'}, inplace=True)
    df_selection = df.groupby("Country_of_Origin").agg({'Arabica' : 'sum', 'Robusta' : 'sum', 'Clean_Cup':'sum', 'Aroma' : 'mean', 'Flavor' : 'mean', 'Aftertaste' : 'mean', 'Acidity' : 'mean', 'Body' : 'mean', 'Balance' : 'mean', 'Species' : 'unique'}).reset_index()
    
    url = (
        "https://github.com/Kitiara2/repo/raw/main"
    )
    state_geo = f"{url}/world.geojson"
    countries =("https://github.com/Kitiara2/repo/raw/main/country.csv")
    df_countries = pd.read_csv(countries)
    df_lands = pd.merge(df_countries, df_selection, left_on = 'value', right_on = 'Country_of_Origin')
    df_lands
    
    ""
    "Посмотрим, где добывают кофе"
    "(здесь можно выбрать сорт зёрен, поменять масштаб или передвинуть карту)"
    ""
    
    species = st.selectbox(
        "Species", ["Arabica", "Robusta"]
    )
    df_lands_selection = df_lands[lambda x: x[species] > 0]
    df_lands_selection

    m = folium.Map(location=[48, -102], zoom_start=1)
    
    folium.Choropleth(
        geo_data=state_geo,
        name="choropleth",
        data=df_lands_selection,
        columns=["id", "Clean_Cup"],
        key_on="feature.properties.WB_A2",
        fill_color="YlGn" if species == 'Arabica' else "PuOr",
        fill_opacity=0.7,
        nan_fill_opacity = 0,
        line_opacity=0.2,
        legend_name="Clean_Cup",
    ).add_to(m)

    folium.LayerControl().add_to(m)
    st_data = st_folium(m, width = 725)
    st_data
    
    ""
    "На карте агрегированы данные за все представленные в датасете года, но давайте посмотрим на динамику"
    "(На следующем графике можно увидеть статистику по годам. В качестве главных характеристик партии выбраны вкус и аромат кофе."
    
    df_years = df
    trace_list = []
    
    for year in list(set(df_years["harvest_year"])):
        df_years_selection = df[lambda x: x["harvest_year"] == year]
        trace_list.append(go.Scatter(visible=False, x=df_years_selection['Flavor'], y=df_years_selection['Aroma'], mode='markers', name = "cups", marker=dict(size=2*df_years_selection['Clean_Cup'])))
    
    fig = go.Figure(data=trace_list)
    fig.update_layout(title="Характеристики поставок",
                  xaxis_title="Вкус",
                  yaxis_title="Аромат",
                  margin=dict(l=0, r=0, t=30, b=0))
    
    num_steps = len(set(df_years["harvest_year"]))
    steps = []
    for i in range(num_steps):
        step = dict(
            method = 'restyle',  
            args = [{'visible': [False] * len(fig.data)},
                   {"title": "Slider switched to step: " + str(i)}],
        )
        step['args'][0]['visible'][i] = True
        
        # Add step to step list
        steps.append(step)
        
    sliders = [dict(
        steps = steps,
    )]

    fig.layout.sliders = sliders
    st.plotly_chart(fig)
    
    ""
    "Теперь посмотрим на данные по отдельным странам"
    "Цвет точек соответствует оценке баланса всех его показателей"
    ""
    
    country = st.selectbox(
        "Country", df["Country_of_Origin"].value_counts().iloc[:30].index
    )

    df_selection = df[lambda x: x["Country_of_Origin"] == country]
    df_selection

    chart = (
        alt.Chart(df_selection)
        .mark_circle()
        .encode(x=alt.X("harvest_year:T"), y="Number_of_Bags", color = "Balance:Q")
    )

    st.altair_chart(
        (
            chart
            + chart.transform_loess("harvest_year", "Number_of_Bags").mark_line()
        ).interactive()
    )

    
    ""
    "Теперь посмотрим на регионы, в которых добывается кофе."
    "При наведении на точку можно узнать конкретную страну, в которой собрали партию, обозначенную ей"
    ""
    region = st.selectbox(
        "Region", df["Region"].value_counts().iloc[:30].index
    )
    
    
    df_selection = df[lambda x: x["Region"] == region]
    df_selection = df_selection.groupby(["Country_of_Origin", "harvest_year", "Species"]).sum().reset_index()
    df_selection

    chart = (
        alt.Chart(df_selection)
        .mark_circle()
        .encode(x=alt.X("harvest_year:T"), y="Clean_Cup", tooltip="Country_of_Origin", color = "Species")
    )

    st.altair_chart(
        (
            chart
        ).interactive()
    )

    species = st.selectbox(
        "Species_1", df["Species"].value_counts().iloc[:10].index
    )
    
    ""
    "Последний график показывает распределение добычи каждого вида кофе по странам, его добывающим"
    ""

    df_selection = df[lambda x: x["Species"] == species]
    df_selection = df_selection.drop("harvest_year", 1).groupby("Country_of_Origin").sum().reset_index()
    df_selection

    base = (
        alt.Chart(df_selection)
        .encode(
            theta=alt.Theta("Clean_Cup:Q", stack=True),
            radius=alt.Radius("Clean_Cup", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
            color="Body:N",
        )
    )

    c1 = base.mark_arc(innerRadius=20, stroke="#fff")

    c2 = base.mark_text(radiusOffset=10).encode(text="Clean_Cup:Q")

    c1 + c2


    
