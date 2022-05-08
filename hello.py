import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

with st.echo(code_location='below'):
    """
    ## Hello, World!
    """


    def print_hello(name="World"):
        st.write(f"### Hello, {name}!")


    name = st.text_input("Your name", key="name", value="Anonymous")
    print_hello(name)

    """
    ## Добавим графики
    Чтобы заработали библиотеки seaborn и altair, нужно добавить в проект файл 
    `requirements.txt` с такими строчками:
    
        seaborn
        altair
    """


    a = st.slider("a")
    x = np.linspace(-6, 6, 500)
    df = pd.DataFrame(dict(x=x, y=np.sin(a * x)))
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="x", y="y", ax=ax)
    st.pyplot(fig)

    """
    ## Немного анализа данных
    """


    @st.cache
    def get_data(data_url):
#        data_url = "file://localhost/C:/Users/kitiara/Desktop/streamlit-example2022-master/arabica_data_cleaned.csv"
            

        
        return (
            pd.read_csv(data_url)
            .assign(
                harvest_year=lambda x: pd.to_datetime(
                    x["Harvest.Year"], format="%Y", errors='coerce'
                    )
            )
        ).drop("Harvest.Year", 1)


    df_ro = get_data("https://github.com/Kitiara2/repo/blob/main/robusta_data_cleaned.csv")
    df_ro.rename(columns={'Country_of_Origin': 'Country.of.Origin', 'Clean_Cup': 'Clean.Cup'}, inplace=True)
    df_ar = get_data("https://github.com/Kitiara2/repo/blob/main/arabica_data_lite.csv")

    df = pd.concat([df_ar, df_ro], ignore_index=False)
#    df = df_ro
    st.write(df)

    df.rename(columns={'Clean.Cup': 'Clean_Cup'}, inplace=True)
    df.rename(columns={'Country.of.Origin': 'Country_of_Origin'}, inplace=True)

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



    
