#import Libraries yang diperlukan
from tokenize import String
from matplotlib.pyplot import text
import streamlit as st
import pandas as pd
import numpy as np
from turtle import width
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns


# Membangun aplikasi dashboard
# image = Image.open("Health.jpeg")
#st.image(image, width=500)
st.markdown('<style>body{background-color: lightblue}</style>', unsafe_allow_html=True)
st.header("""
Analisis Dashboard Penyebab Kematian Di Dunia ☠️
""")

# Import Dataset
@st.cache
def load_data():
    df = pd.read_csv("cd.csv")
    return df

df = load_data()

state_select = st.sidebar.selectbox('Select a Country', df['Entity'].unique())
selected_state = df[df['Entity'] == state_select]

column_names = ["Entity","Code","Year","Causes name","Causes Full Description","Death Numbers"]

selected_state = selected_state.reindex(columns=column_names)

fig = px.bar(selected_state, x='Year', y='Death Numbers',
            hover_data=['Code', 'Causes Full Description'], color='Causes name',
            labels={'Death Numbers':'Total Death'}, height=400 , width=1200)
st.plotly_chart(fig)

scatter_fig = px.scatter(selected_state, x='Year' ,  y='Death Numbers', hover_data=['Code', 'Causes Full Description'], color='Causes name', height=400 , width=1200) 
st.plotly_chart(scatter_fig)

Cause_select = st.selectbox('Pilih Penyebab' , selected_state['Causes name'].sort_values(ascending=True).unique())
selected_cause = selected_state[selected_state['Causes name'] == Cause_select]

df4 = selected_cause.sort_values(by=['Year'])

df5 = df4.replace(np.nan,0)

fig4 = px.line(df5,x='Year' , y='Death Numbers',title=f"Total Death by {Cause_select}")
st.plotly_chart(fig4)

fig_scatter = px.scatter(selected_cause, x="Year", y="Death Numbers" , color="Entity" ,hover_data=['Causes name'] )
st.plotly_chart(fig_scatter)

#Menambahkan Title Sum dari Total kematian akibat penyebab 
fig2 = px.bar(df5, x='Causes name', y='Death Numbers',
             hover_data=['Code', 'Death Numbers','Year'],color='Causes name',
             labels={'Death Numbers':'Total Death'}, height=400 , width=400)
st.plotly_chart(fig2)

df8=df5.pivot_table(index=['Causes name'],values=['Death Numbers'],aggfunc=sum).iloc[[0],[0]].values
st.write(f"Total deaths Caused by {Cause_select} From 1990 - 2019 in {state_select} : " , str(int(df8)))

year_select = st.selectbox('Select Year' , selected_cause['Year'].sort_values(ascending=True).unique())
selected_year = selected_state[selected_state['Year'] == year_select]

fig3 = px.bar(selected_year, x='Year', y='Death Numbers',
             hover_data=['Code', 'Death Numbers'],color='Causes name',
             labels={'Death Numbers':'Total Death by diseases & accidents'}, height=400, width=650)
st.plotly_chart(fig3)

df9=selected_year.pivot_table(index=['Year'],values=['Death Numbers'],aggfunc=sum).iloc[[0],[0]].values
st.write(f"Total deaths in {state_select} in Year {year_select}: " , str(int(df9)))