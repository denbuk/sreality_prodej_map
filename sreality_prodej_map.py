from collections import namedtuple
from datetime import datetime as dt
from PIL import Image
# import pyparsing
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st
import requests
import json
from google.oauth2 import service_account
from gsheetsdb import connect

with st.echo(code_location='below'):
    st.title('Adobe tag generator')
    with st.spinner('Wait for it...'):
        time.sleep(2)
        
# streamlit_app.py

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
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write("{row.name}")

   
