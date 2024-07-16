import os
import pandas as pd
import streamlit as st
import requests
from google.oauth2 import service_account

# Replace with your Google Drive folder ID or leave it empty
FOLDER_ID = "your-folder-id"  # Optional

# Define your Streamlit app
def upload_to_drive(file_name):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    SERVICE_ACCOUNT_FILE = 'path/to/your/service_account.json'  # For Streamlit Cloud, use env variables

    # Use service account
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Uploading the file
    headers = {"Authorization": f"Bearer {credentials.token}"}
    file_metadata = {
        'name': file_name,
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [FOLDER_ID] if FOLDER_ID else []
    }
    
    # Create the file
    response = requests.post(
        'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
        headers=headers,
        json=file_metadata,
        files={'file': open(file_name, 'rb')}
    )

    return response.json()

# Streamlit interface
if st.button('Upload CSV to Google Drive'):
    df = pd.DataFrame({'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']})
    csv_file = 'data.csv'
    df.to_csv(csv_file, index=False)

    result = upload_to_drive(csv_file)
    st.write(result)