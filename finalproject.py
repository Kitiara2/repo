import streamlit as st

with st.echo(code_location='below'):
  st.write("hello")
  

df = get_data("https://github.com/Kitiara2/repo/raw/main/investments_VC.csv")
df
