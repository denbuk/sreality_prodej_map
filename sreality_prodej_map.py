import streamlit as st
import requests
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # This creates a local webserver for authentication
drive = GoogleDrive(gauth)

# Sample DataFrame
df = pd.DataFrame({
    'Column1': [1, 2, 3],
    'Column2': ['A', 'B', 'C']
})

# Save to CSV
csv_file = 'data.csv'
df.to_csv(csv_file, index=False)

# Upload to Google Drive
file = drive.CreateFile({'title': csv_file})
file.SetContentFile(csv_file)
file.Upload()

st.write("CSV saved to Google Drive successfully!")