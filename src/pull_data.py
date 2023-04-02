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
