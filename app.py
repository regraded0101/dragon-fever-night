import subprocess
import streamlit as st
import pandas as pd

data_month_year = pd.read_csv('data/france_regions_weather_data.csv')

convert_months = {
    1:"Jan",
    2:"Feb",
    3:"Mar",
    4:"Apr",
    5:"May",
    6:"Jun", 
    7:"July",
    8:"Aug",
    9:"Sep",
    10:"Oct",
    11:"Nov",
    12:"Dec"
}

data_month_year['month'] = data_month_year['month'].replace(convert_months)

selected_wine_region = st.sidebar.selectbox("Wine Region", options=data_month_year["location"].unique())
selected_year = st.sidebar.selectbox("Year", options=data_month_year["year"].sort_values(ascending=False).unique())

plot_data = data_month_year[(data_month_year['year'] == selected_year) & (data_month_year['location'] == selected_wine_region)]


import plotly.graph_objects as go
from plotly.subplots import make_subplots


fig = go.Figure()

fig.add_trace(go.Scatter(x = plot_data['month'], y = plot_data['tmax'], name="Max Temp", line_color="#F17720"))
fig.add_trace(go.Scatter(x=plot_data['month'], y=plot_data["tmax_month"], name="Max Temp (Monthly Average)", line_dash="dash", line_color="#F17720", opacity=0.5))
fig.add_trace(go.Scatter(x = plot_data['month'], y = plot_data['tmin'], name="Min Temp", line_color="#0474BA"))
fig.add_trace(go.Scatter(x=plot_data['month'], y=plot_data["tmin_month"], name="Min Temp (Monthly Average)", line_dash="dash", line_color="#0474BA", opacity=0.5))

fig.update_layout(
    #plot_bgcolor='#FFFFFF',
        yaxis=dict(range=[-10, 45],
                   showticklabels=False,
                   showgrid=False
                   )
)
fig.add_vline(
    x = 'Mar',
    line_dash = 'dash',
)
fig.add_annotation(
    x="Mar",
    y = 45,
    text="Growth Cycle Start",
    showarrow=False
)
fig.add_vline(
    x='Oct',
    line_dash='dash',
)
fig.add_annotation(
    x = 'Oct',
    y = 45,
    text = 'Harvest',
    showarrow=False
)

st.plotly_chart(fig)