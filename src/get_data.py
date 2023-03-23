from geopy.geocoders import Nominatim
from meteostat import Stations, Daily

def get_lat_long(place):
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode('Champagne, France')
    return loc

def get_nearest_station_id(lat_long):
    stations = Stations()
    stations = stations.nearby(lat_long.latitude, lat_long.longitude)
    station = stations.fetch(1)
    return station

def get_weather_data(station_id, start_date, end_date):
    
    # Get Daily data
    data = Daily(station_id.index.values[0], start_date, end_date)
    data = data.fetch()
    data = data.reset_index()
    data = data[['time','tavg', 'tmin', 'tmax']]

    return data


