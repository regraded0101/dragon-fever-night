import plotly.graph_objects as go
import plotly.express as px


def plotTimeSeries(plot_data):
    """
    Function to return the temp time series
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=plot_data["month"],
            y=plot_data["tmax"],
            name="Max Temp",
            line_color="#F17720",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=plot_data["month"],
            y=plot_data["tmax_month"],
            name="Max Temp (Monthly Average)",
            line_dash="dash",
            line_color="#F17720",
            opacity=0.5,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=plot_data["month"],
            y=plot_data["tmin"],
            name="Min Temp",
            line_color="#0474BA",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=plot_data["month"],
            y=plot_data["tmin_month"],
            name="Min Temp (Monthly Average)",
            line_dash="dash",
            line_color="#0474BA",
            opacity=0.5,
        )
    )

    fig.update_layout(
        yaxis=dict(range=[-10, 45], showticklabels=False, showgrid=False),
        legend=dict(x=-0.1, y=1.4, traceorder="normal", orientation="v"),
    )

    fig.add_vline(
        x="Mar",
        line_dash="dash",
    )

    fig.add_vline(
        x="Oct",
        line_dash="dash",
    )
    fig.add_annotation(x="Jun", y=45, text="Grape Growing Season", showarrow=False)

    return fig


def plotStationsMap(stations_data, selected_wine_region):
    """
    Function to return weather stations map plot
    """

    mapData = stations_data[stations_data["wine_region"] == selected_wine_region]
    fig_map = px.scatter_geo(
        mapData,
        lon="longitude",
        lat="latitude",
        scope="europe",
        hover_data=["hover_text"],
        title=f"Weather Station Data for {selected_wine_region.replace(', France','')}",
    )

    # Set the zoom level
    fig_map.update_layout(
        geo=dict( 
            scope="europe", projection_scale=3, center=dict(lat=41.557414, lon=5.748498)
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        title={"x": 0.28, "y": 0.95},
    )

    fig_map.update_traces(hovertemplate="%{customdata[0]}")
    return fig_map
