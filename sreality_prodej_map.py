import streamlit as st
import requests
import pandas as pd
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
def main():
    st.title("Fetch Data from API Example")

    # Input for the API endpoint
    endpoint = st.text_input("Enter the API endpoint URL:")

    if st.button("Fetch Data"):
        if endpoint:
            data = fetch_data(endpoint)
            if data:
                # Display data
                st.write(data)

                # Convert to DataFrame for better display
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                elif isinstance(data, dict):
                    df = pd.DataFrame([data])
                    st.dataframe(df)
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()