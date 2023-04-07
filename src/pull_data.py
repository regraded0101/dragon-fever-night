import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd

def pullData():
    '''
    function to pull data from google sheets - needs breaking up!
    
    '''

    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )
    conn = connect(credentials=credentials)

    # Perform SQL query on the Google Sheet.
    # Uses st.cache_data to only rerun when the query changes or after 10 min.
    @st.cache_data(ttl=600)
    def run_query(query):
        rows = conn.execute(query, headers=1)
        rows = rows.fetchall()
        return rows

    sheet_url = st.secrets["private_gsheets_url"]

    df = pd.read_sql(f'SELECT * FROM "{sheet_url}"', conn)
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)

    return df


def formatData(df):
    """
    function to format the months from numbers to months
    requires a column called 'months' with numerical values (1 - 12)
    """

    convert_months = {
        1:"Jan",
        2:"Feb",
        3:"Mar",
        4:"Apr",
        5:"May",
        6:"Jun", 
        7:"Jul",
        8:"Aug",
        9:"Sep",
        10:"Oct",
        11:"Nov",
        12:"Dec"
    }

    df['month'] = df['month'].replace(convert_months)

    return df

def percentageDiff(new, old):
    return 100*(new - old)/old 

def getTempStats(df, selected_year, selected_wine_region):

    """
    Function to return min, max and avg temperature for a year and region
    Returns a list of lists of values, structured [[avg], [min], [max]]
    """
    # only look at wine growing months (northern hemisphere)
    growing_months = [
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct"
    ]
    avg_values_data = df[df['month'].isin(growing_months)]
     

    avg_values_data = avg_values_data[(avg_values_data['year'] == selected_year) & 
                                      (avg_values_data['location'] == selected_wine_region)]

    avg_growing_temp = avg_values_data['tavg'].mean()
    avg_growing_temp_monthly = avg_values_data['tavg_month'].mean()

    min_growing_temp = avg_values_data['tmin'].min()
    min_growing_temp_monthly = avg_values_data['tmin_month'].min()

    max_growing_temp = avg_values_data['tmax'].max()
    max_growing_temp_monthly = avg_values_data['tmax_month'].max()

    return avg_growing_temp, avg_growing_temp_monthly, min_growing_temp, min_growing_temp_monthly, max_growing_temp, max_growing_temp_monthly





# data_month_year = pullData()
# data_month_year = formatData(df = data_month_year)
# print(data_month_year)

