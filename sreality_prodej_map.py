import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd
import plotly.express as px

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
# @st.cache_data(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

#sheet_id = "1l5YgElKRpM1trDFaIY-q-rAJ2OaPHLhTBVVQ0Ed0aeQ"
#sheet_name = "sreality-api-first-prodej"
#url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

#worksheet = conn.worksheet(sheet_url)
#rows = worksheet.get_all_records()

# Print results.
df = pd.DataFrame(rows)

fig = px.scatter_mapbox(df, lat="lat", lon="lon", color="price", hover_name="name", color_continuous_scale=px.colors.cyclical.IceFire, zoom=3)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)
#st.table(df)
#df.columns = ['name', 'lat', 'lon']


#st.map(df)