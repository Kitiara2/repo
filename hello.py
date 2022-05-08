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
import json
import folium
#import webbrowser

with st.echo(code_location='below'):



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
    df_ar = get_data("https://github.com/Kitiara2/repo/raw/main/arabica_data_cleaned.csv")

    df = pd.concat([df_ar, df_ro], ignore_index=False)
#    df = df_ro
    st.write(df)
    df.rename(columns={'Country.of.Origin': 'Country_of_Origin'}, inplace=True)
    df.rename(columns={'Clean.Cup': 'Clean_Cup'}, inplace=True)
    df_selection = df.groupby(["Country_of_Origin", "harvest_year", "Species"]).sum().reset_index()
    
    url = (
        "https://github.com/Kitiara2/repo/raw/main"
    )
    state_geo = f"{url}/countries-land.geo.json"
    countries =("https://github.com/Kitiara2/repo/raw/main/country.csv")
    df_countries = pd.read_csv(countries)
    df_lands = pd.merge(df_countries, df_selection, left_on = 'value', right_on = 'Country_of_Origin')
    df_lands
#    state_data = pd.read_csv(state_unemployment)

    m = folium.Map(location=[48, -102], zoom_start=3)

    folium.Choropleth(
        geo_data=state_geo,
        name="choropleth",
        data=df_countries,
        columns=["id", "Clean_Cup"],
        key_on="feature.geometry.properties.A3",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Clean_Cup",
    ).add_to(m)

    folium.LayerControl().add_to(m)

    
    st_data = st_folium(m, width = 725)
    st_data


    country = st.selectbox(
        "Country", df["Country_of_Origin"].value_counts().iloc[:10].index
    )

    df_selection = df[lambda x: x["Country_of_Origin"] == country]
    df_selection = df
    df_selection

    chart = (
        alt.Chart(df_selection)
        .mark_circle()
        .encode(x=alt.X("harvest_year:T"), y="Number_of_Bags")
    )

    st.altair_chart(
        (
            chart
            + chart.transform_loess("harvest_year", "Number_of_Bags").mark_line()
        ).interactive()
        # .transform_loess добавляет сглаживающую кривую
    )

    region = st.selectbox(
        "Region", df["Region"].value_counts().iloc[:10].index
    )


    df_selection = df[lambda x: x["Region"] == region]
    df_selection = df.groupby(["Country_of_Origin", "harvest_year", "Species"]).sum().reset_index()
    df_selection

    chart = (
        alt.Chart(df_selection)
        .mark_circle()
        .encode(x=alt.X("harvest_year:T"), y="Clean_Cup", tooltip="Country_of_Origin", color = "Species")
    )

    st.altair_chart(
        (
            chart
#            + chart.transform_loess("harvest_year", "Clean_Cup").mark_line()
        ).interactive()
        # .transform_loess добавляет сглаживающую кривую
    )

    species = st.selectbox(
        "Species", df["Species"].value_counts().iloc[:10].index
    )


    df_selection = df[lambda x: x["Species"] == species]
    df_selection = df.drop("harvest_year", 1).groupby("Country_of_Origin").sum().reset_index()
    df_selection

    base = (
        alt.Chart(df_selection)
        .encode(
            theta=alt.Theta("Clean_Cup:Q", stack=True),
            radius=alt.Radius("Clean_Cup", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
            color="Clean_Cup:N",
        )
    )

    c1 = base.mark_arc(innerRadius=20, stroke="#fff")

    c2 = base.mark_text(radiusOffset=10).encode(text="Clean_Cup:Q")

    c1 + c2


    
