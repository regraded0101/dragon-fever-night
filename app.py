import subprocess

import streamlit as st
import pandas as pd


data_month_year = pd.read_csv('data/france_regions_weather_data.csv')
# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
# def load_data(sheets_url):
#     csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
#     return pd.read_csv(csv_url)

# df = load_data(st.secrets["public_gsheets_url"])


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
def align_region_names(x):
    if x == "Rhône Valley, France":
        return "Rhône, France"
    elif x in ["Beaujolais, France", "Burgundy, France", "Chablis, France"]:
        return "Bourgogne, France"
    elif x in ["Bugey Savoie, France", "Corsica, France"]:
        return "Not yet mapped"
    elif x == "Languedoc, France":
        return "Languedoc-Roussillon, France"
    elif x == "Loire Valley, France":
        return "Loire, France"
    else:
        return x

data_month_year['name_mapped'] = data_month_year["location"].map(align_region_names)


import geopandas as gpd
import folium
import requests


# URL of the raw GeoJSON file in the GitHub repository
geojson_url = "https://raw.githubusercontent.com/UCDavisLibrary/wine-ontology/master/examples/france/regions.geojson"

# Send an HTTP GET request to retrieve the GeoJSON data
response = requests.get(geojson_url)

# Check if the response was successful (i.e. the status code is 200)
if response.status_code == 200:
        # Get the GeoJSON data from the response
    geojson_data = response.json()

    # Read the GeoJSON data into a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])

else:
    # Print an error message if the response was not successful
    print("Error retrieving GeoJSON data from GitHub repository.")

gdf['region'] = gdf['region'].str.replace('Region |region ', '')
gdf['region'] = gdf['region'] + ', France'
gdf.crs = geojson_data["crs"]["properties"]["name"]

m = folium.Map(location=[gdf.centroid.y.mean(), gdf.centroid.x.mean()], zoom_start=5)
# Create a choropleth layer based on a column in the GeoPandas object
folium.GeoJson(
    gdf,
    tooltip=folium.GeoJsonTooltip(fields=['region']),
    style_function=lambda feature: {'fillColor':'#808080', 
                                                'fillOpacity':0.9, 'weight':0}
).add_to(m)





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

from streamlit_folium import st_folium

st_folium(m)