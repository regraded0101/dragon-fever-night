import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


from src.pull_data import pullGSheets, formatData, percentageDiff, getTempStats
from src.pull_plots import plotTimeSeries, plotStationsMap

st.set_page_config(page_title="French Wine Weather")


@st.cache_data
def pull_data():
    data_month_year, stations_data = pullGSheets()
    data_month_year = formatData(df=data_month_year)

    return data_month_year, stations_data


data_month_year, stations_data = pull_data()

##### INPUTS
selected_wine_region = st.sidebar.selectbox(
    "Wine Region", options=data_month_year["location"].unique()
)
selected_year = st.sidebar.selectbox(
    "Year", options=data_month_year["year"].sort_values(ascending=False).unique()
)
#####


(
    avg_growing_temp,
    avg_growing_temp_monthly,
    min_growing_temp,
    min_growing_temp_monthly,
    max_growing_temp,
    max_growing_temp_monthly,
) = getTempStats(
    df=data_month_year,
    selected_year=selected_year,
    selected_wine_region=selected_wine_region,
)


plot_data = data_month_year[
    (data_month_year["year"] == selected_year)
    & (data_month_year["location"] == selected_wine_region)
]


time_series_plot = plotTimeSeries(plot_data=plot_data)
station_map_plot = plotStationsMap(
    stations_data=stations_data, selected_wine_region=selected_wine_region
)

##### OUTPUTS
with st.expander("Instructions"):
    st.write(
        """
        Open the sidebar panel on the left and input the wine region and year of the wine to get temperatures from nearby weather stations and how they compare to averages across multiple years.\n
        If you cannot see the sidebar, press on the arrow at the top of this page to open the sidebar.
        Higher temperatures mean riper grapes earlier and a change in the wine's flavour!
    """
    )

col1, col2, col3 = st.columns(3)


col1.metric(
    "Average Growing Temperature",
    f"{round(avg_growing_temp,1)} {chr(176)}",
    f"{round(percentageDiff(avg_growing_temp, avg_growing_temp_monthly),1)}%",
)

col2.metric(
    "Minimum Growing Temperature",
    f"{round(min_growing_temp,1)} {chr(176)}",
    f"{round(percentageDiff(min_growing_temp, min_growing_temp_monthly),1)}%",
)

col3.metric(
    "Maximum Growing Temperature",
    f"{round(max_growing_temp,1)} {chr(176)}",
    f"{round(percentageDiff(max_growing_temp, max_growing_temp_monthly),1)}%",
)

st.plotly_chart(time_series_plot, use_container_width=True)

st.plotly_chart(station_map_plot, use_container_width=True)
#####
