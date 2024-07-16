import streamlit as st
import requests
import pandas as pd
import os
import json

st.write("Current Directory:", os.getcwd())

# Define the path for the CSV file
csv_file_path = 'data.csv'

# Function to save data to CSV
def save_to_csv(estates):
    # Check if the CSV file exists
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
    else:
        df = pd.DataFrame(columns=['id', 'name', 'price'])  # Adjust columns as needed

    # Create a DataFrame from the estates list
    estates_df = pd.DataFrame(estates)
    
    # Append new data
    df = pd.concat([df, estates_df], ignore_index=True)
    
    # Save to CSV
    df.to_csv(csv_file_path, index=False)
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
            if data and '_embedded' in data and 'estates' in data['_embedded']:
                estates = data['_embedded']['estates']
                save_to_csv(estates)
                st.success("Data saved to CSV successfully!")

                # Display the estates
                df = pd.DataFrame(estates)
                st.dataframe(df)
            else:
                st.warning("No estates found in the response.")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()