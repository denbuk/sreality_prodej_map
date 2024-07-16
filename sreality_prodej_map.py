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
    creds = ServiceAccountCredentials.from_json_keyfile_name("path_to_your_credentials.json", scope)

    # Authorize the clientsheet 
    client = gspread.authorize(creds)

    # Get the instance of the Spreadsheet
    sheet = client.open(sheet_name)

    # Get the first sheet of the Spreadsheet
    worksheet = sheet.get_worksheet(0)

    # Clear existing data
    worksheet.clear()

    # Prepare the data to be written
    if isinstance(data, list):
        # Assuming data is a list of dictionaries
        keys = data[0].keys()
        worksheet.append_row(keys)
        for row in data:
            worksheet.append_row(row.values())
    elif isinstance(data, dict):
        # Assuming data is a single dictionary
        worksheet.append_row(data.keys())
        worksheet.append_row(data.values())
    else:
        st.error("Unsupported data format")

# Streamlit app layout
st.title("Fetch and Save Data")

endpoint = st.text_input("API Endpoint", "https://api.example.com/data")
sheet_name = st.text_input("Google Sheet Name", "Your Google Sheet Name")

if st.button("Fetch and Save"):
    data = fetch_data(endpoint)
    if data:
        save_to_google_sheets(data, sheet_name)
        st.success("Data saved to Google Sheets successfully")