import csv
import pandas as pd
from geopy.geocoders import Nominatim
from meteostat import Stations, Daily

class FetchData():

    def __init__(self, place, start_date, end_date):
        self.place = place
        self.start_date = start_date
        self.end_date = end_date



    def get_lat_long(self):
        geolocator = Nominatim(user_agent="my_user_agent")
        loc = geolocator.geocode(self.place)
        return loc

    def get_nearest_station_id(self, loc):
        stations = Stations()
        stations = stations.nearby(loc.latitude, loc.longitude)
        station = stations.fetch(1)
        return station

    def get_weather_data(self):
        
        # Get Daily data
        loc = self.get_lat_long()
        station_id = self.get_nearest_station_id(loc)

        data = Daily(station_id.index.values[0], self.start_date, self.end_date)
        data = data.fetch()
        data = data.reset_index()
        data = data[['time','tavg', 'tmin', 'tmax']]
        data['location'] = self.place

        return data



def get_summary_stats(data):
    """
    Function to create the average temperatures by month-year and just by month 
    """

    data['year'] = data['time'].dt.year
    data['month'] = data['time'].dt.month
    data_month_year = data.groupby(['year', 'month', 'location'])[['tavg', 'tmin', 'tmax']].mean().reset_index()

    data_month = data_month_year.groupby(['month', 'location'])[['tavg', 'tmin', 'tmax']].mean().reset_index()
    data_month.columns = ['month', 'location', 'tavg_month', 'tmin_month', 'tmax_month']
    data_month_year = data_month_year.merge(data_month, how = 'left', on = ['month', 'location'])

    return data_month_year

if __name__ == '__main__':
    with open('data/france-wine-regions.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        places = [row[0] for row in reader]
        places = places[1:] # drop the header

    weather_data = pd.DataFrame()

    for place in places:
        print(f'Attempting: {place}')
        
        daily_weather_data = FetchData(place, '2001-01-01', '2022-12-31').get_weather_data()
        monthly_weather_data = get_summary_stats(daily_weather_data)
        weather_data = pd.concat([weather_data, monthly_weather_data])
        print('Success')
    
    weather_data.to_csv('data/france_regions_weather_data.csv', index=False)
