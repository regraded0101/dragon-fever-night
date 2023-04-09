import csv
import glob

import pandas as pd
from geopy.geocoders import Nominatim
from meteostat import Stations, Daily


class FetchData:
    def __init__(self, place, start_date, end_date):
        self.place = place
        self.start_date = start_date
        self.end_date = end_date

    def get_lat_long(self):
        geolocator = Nominatim(user_agent="my_user_agent")
        loc = geolocator.geocode(self.place)
        return loc

    def get_close_station_ids(self, loc, search_distance=75000):
        stations = Stations()
        stations = stations.nearby(loc.latitude, loc.longitude)
        station = stations.fetch()

        # only return stations within 50kms
        station = station[station["distance"] <= search_distance]
        try:
            if len(station) == 0:
                raise ValueError(
                    f"No weather stations near {self.place} could be found.\nIgnoring, increase the `search_distance` argument to find weather stations.\nCurrent set at {search_distance}"
                )
            return station
        except ValueError as error:
            print("Warning: ", str(error))
            pass

    def get_all_weather_data(self):
        # Get Daily data
        loc = self.get_lat_long()
        station_id = self.get_close_station_ids(loc, search_distance=75000)
        if station_id is not None:
            data_list = []
            for j in range(len(station_id.index)):
                point_data = Daily(
                    station_id.index.values[j], self.start_date, self.end_date
                )
                point_data = point_data.fetch()

                point_data = point_data.reset_index()
                point_data = point_data[["time", "tavg", "tmin", "tmax"]]
                point_data["location"] = self.place

                # drop any rows where time, tav, tmin, tmax are NA
                point_data = point_data[
                    (~point_data["tavg"].isna())
                    | (~point_data["tmin"].isna())
                    | (~point_data["tmax"].isna())
                    | (~point_data["time"].isna())
                ]

                data_list.append(point_data)

            return data_list
        else:
            return None

    def combine_weather_data(self):

        weather_data_list = self.get_all_weather_data()
        if weather_data_list is not None:
            output_data = pd.DataFrame(columns=weather_data_list[0].columns)

            # create a list of all dates that can be removed when date has already been found
            date_list = pd.date_range(start=self.start_date, end=self.end_date)

            for k in range(len(weather_data_list)):
                # only select values that are in the date_list so haven't yet been populated
                weather_data_list[k] = weather_data_list[k][
                    weather_data_list[k]["time"].isin(date_list)
                ]

                output_data = pd.concat([output_data, weather_data_list[k]])

                # update date list to drop dates already included
                date_list = date_list[~date_list.isin(weather_data_list[k]["time"])]

            return output_data
        else:
            return None


def get_summary_stats(data):
    """
    Function to create the average temperatures by month-year and just by month
    """
    if data is not None:
        data["year"] = data["time"].dt.year
        data["month"] = data["time"].dt.month
        data_month_year = (
            data.groupby(["year", "month", "location"])[["tavg", "tmin", "tmax"]]
            .mean()
            .reset_index()
        )

        data_month = (
            data_month_year.groupby(["month", "location"])[["tavg", "tmin", "tmax"]]
            .mean()
            .reset_index()
        )
        data_month.columns = ["month", "location", "tavg_month", "tmin_month", "tmax_month"]
        data_month_year = data_month_year.merge(
            data_month, how="left", on=["month", "location"]
        )

        return data_month_year
    else:
        return None


if __name__ == "__main__":
    # read in all -wine-regions.csv files in data/
    pattern = "data/*-wine-regions.csv"
    matches = glob.glob(pattern)

    places = []
    for match in matches:
        with open(match, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            match_places = [row[0] for row in reader]
            match_places = match_places[1:]  # drop the header
            places.extend(match_places)

    start = "2000-01-01"
    end = "2022-12-31"
    weather_data = pd.DataFrame()

    for place in places:
        print(f"Attempting: {place}")

        daily_weather_data = FetchData(place, start, end).combine_weather_data()
        monthly_weather_data = get_summary_stats(daily_weather_data)
        weather_data = pd.concat([weather_data, monthly_weather_data])
        print("Success")

    weather_data.to_csv("data/regions_weather_data.csv", index=False)

    station_data = pd.DataFrame()
    print("Creating weather stations data...")

    for place in places:
        stationClass = FetchData(place, start, end)
        stationClassLoc = stationClass.get_lat_long()
        placeStationData = stationClass.get_close_station_ids(stationClassLoc)
        placeStationData["hover_text"] = placeStationData.apply(
            lambda x: f'<b>{x["name"]}</b><br>Latitude: {x["latitude"]}<br>Longitude: {x["longitude"]:,}<br>Elevation: {x["elevation"]}',
            axis=1,
        )
        placeStationData["wine_region"] = place
        station_data = pd.concat([station_data, placeStationData])

    print("Finished created weather stations data")
    station_data.to_csv("data/weather-stations.csv", index=False)
