import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


from src.pull_data import pullData, formatData, percentageDiff, getTempStats

st.set_page_config(page_title='French Wine Weather')


data_month_year = pullData()
data_month_year = formatData(df=data_month_year)

selected_wine_region = st.sidebar.selectbox("Wine Region", options=data_month_year["location"].unique())
selected_year = st.sidebar.selectbox("Year", options=data_month_year["year"].sort_values(ascending=False).unique())




avg_growing_temp, avg_growing_temp_monthly, min_growing_temp, min_growing_temp_monthly, max_growing_temp, max_growing_temp_monthly = getTempStats(df=data_month_year,
                            selected_year=selected_year,
                            selected_wine_region=selected_wine_region)


plot_data = data_month_year[(data_month_year['year'] == selected_year) & 
                            (data_month_year['location'] == selected_wine_region)]





# fig = go.Figure()

# fig.add_trace(go.Scatter(x = plot_data['month'], y = plot_data['tmax'], name="Max Temp", line_color="#F17720"))
# fig.add_trace(go.Scatter(x=plot_data['month'], y=plot_data["tmax_month"], name="Max Temp (Monthly Average)", line_dash="dash", line_color="#F17720", opacity=0.5))
# fig.add_trace(go.Scatter(x = plot_data['month'], y = plot_data['tmin'], name="Min Temp", line_color="#0474BA"))
# fig.add_trace(go.Scatter(x=plot_data['month'], y=plot_data["tmin_month"], name="Min Temp (Monthly Average)", line_dash="dash", line_color="#0474BA", opacity=0.5))


# fig.update_layout(
#         yaxis=dict(range=[-10, 45],
#                    showticklabels=False,
#                    showgrid=False
#                    ),
#         legend=dict(
#                     x=-0.1,
#                     y=1.4,
#                     traceorder='normal',
#                     orientation='v'
#         ),
# )



# fig.add_vline(
#     x = 'Mar',
#     line_dash = 'dash',
# )

# fig.add_vline(
#     x='Oct',
#     line_dash='dash',
# )
# fig.add_annotation(
#     x = 'Jun',
#     y = 45,
#     text = 'Grape Growing Season',
#     showarrow=False
# )



# stationsData = pd.read_csv('data/france-weather-stations.csv')

# mapData = stationsData[stationsData['wine_region'] == selected_wine_region]
# fig_map = px.scatter_geo(
#     mapData,
#     lon="longitude",
#     lat="latitude",
#     scope="europe",
#     hover_data=["hover_text"],
#     title=f"Weather Station Data for {selected_wine_region.replace(', France','')}",
#     )

# # Set the zoom level
# fig_map.update_layout(geo=dict(
#         scope='europe',
#         projection_scale=5,
#         center=dict(lat=46.2276, lon=2.2137)
#     ),
#     margin=dict(l=0, r=0, t=50, b=0),
#     title={
#         "x":0.28,
#         "y":0.95
#     }
# )

# fig_map.update_traces(hovertemplate='%{customdata[0]}')

# with st.expander("Instructions"):
#     st.write("""
#         Open the sidebar panel on the left and input the wine region and year of the wine to get temperatures from nearby weather stations and how they compare to averages across multiple years.\n
#         If you cannot see the sidebar, press on the arrow at the top of this page to open the sidebar.
#         Higher temperatures mean riper grapes earlier and a change in the wine's flavour!
#     """)

col1, col2, col3 = st.columns(3)


col1.metric("Average Growing Temperature", 
            f"{round(avg_growing_temp,1)} {chr(176)}",
            f"{round(percentageDiff(avg_growing_temp, avg_growing_temp_monthly),1)}%")

col2.metric("Minimum Growing Temperature", 
            f"{round(min_growing_temp,1)} {chr(176)}",
            f"{round(percentageDiff(min_growing_temp, min_growing_temp_monthly),1)}%")

col3.metric("Maximum Growing Temperature", 
            f"{round(max_growing_temp,1)} {chr(176)}",
            f"{round(percentageDiff(max_growing_temp, max_growing_temp_monthly),1)}%")

# st.plotly_chart(fig, use_container_width=True)

# st.plotly_chart(fig_map, use_container_width=True)

