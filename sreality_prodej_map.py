import streamlit as st
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Function to fetch data from API endpoint
def fetch_data(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the endpoint")
        return None

# Function to save data to Google Sheets
def save_to_google_sheets(data, sheet_name):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']

    # Add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name("starry-computer-387421-161a86e54e0a.json", scope)

    # Authorize the clientsheet 
    client = gspread.authorize(creds)

    # Get the instance of the Spreadsheet
    #spreadsheet = client.open(sheet_name)

    # Create a new sheet with a unique name
    #new_sheet_name = f"Sheet {len(spreadsheet.worksheets()) + 1}"
    #worksheet = spreadsheet.add_worksheet(title=new_sheet_name, rows="100", cols="20")

    sr_estates_list = data['_embedded']['estates'][0]

    st.write(sr_estates_list)

# Streamlit app layout
st.title("Fetch and Save Data")
''

endpoint = st.text_input("API Endpoint", "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&ownership=1&per_page=5&tms=1721153792&page=5&floor_number=1%7C1&%26no_auction=1&no_shares=1")
sheet_name = st.text_input("Google Sheet Name", "sreality-api-update-2")

if st.button("Fetch and Save"):
    data = fetch_data(endpoint)
    if data:
        
        save_to_google_sheets(data, sheet_name)
        st.success("Data saved to Google Sheets successfully")