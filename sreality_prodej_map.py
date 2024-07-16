import streamlit as st
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

## CREDENTIALS - Custom DEPENDENCIES
CREDENTIALS = {
    "type": "service_account",
    "project_id": "<YOUR-PROJECT-ID>",
    "private_key_id": st.secrets["PRIVATE_KEY_ID"],
    "private_key": st.secrets["PRIVATE_KEY"],
    "client_email": st.secrets["CLIENT_EMAIL"],
    "client_id": st.secrets["CLIENT_ID"],
    "auth_url": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": st.secrets["CLIENT_X509_CERT_URL"]
    }

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_dict(CREDENTIALS, scope)

client = gspread.authorize(credentials)

def update_sheet(client):
    sheet = client.open("streamlit-sreality-v2.0")
    sheet_insurance = sheet.get_worksheet(0)
    sheet_insurance.insert_rows(df.values.tolist())

# => Retrieving Values
def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value


# => Retrieving Values II
def get_fvalue(val):
    feature_dict = {"yes": 1, "no": 0}
    for key, value in feature_dict.items():
        if val == key:
            return value
        
### Dictionary/Labels
sex_map = {'male': 1.0, 'female': 0.0}
smoker_map = {'yes': 1.0, 'no': 0.0}
region_map = {'southeast': 3.0, 'southwest': 4.0,
              'northwest': 2.0, 'northeast': 1.0}

## Page Title
st.title('Real-time Monitoring Streamlit and Google Sheets')

## Attributes
# Age
age = st.sidebar.number_input("Age", 1, 100, 18, 1)
# Sex
sex = st.sidebar.radio("Sex", tuple(sex_map.keys()))
# Region
region = st.sidebar.radio("Region", tuple(region_map.keys()))
# Body Mass Index 
bmi = st.sidebar.number_input("Body Mass Index", 10.00, 100.00, 15.96, 0.10)
# Children
children = st.sidebar.number_input("Number of children", min_value=0, value=1, step=1)
# Smoker
smoker = st.sidebar.radio("Do you Smoke?",tuple(smoker_map.keys()))


# Time
entry_date = datetime.now().strftime("%d-%m-%Y")
entry_dir = 'contrib' + '_' + entry_date

## Feature Values
feature_values = [age, get_value(sex, sex_map),
                  bmi, children, get_fvalue(smoker),
                  get_value(region, region_map)]

### Collect
pretty_results = {'age': [age], 'sex': [sex],
                  'bmi': [bmi], 'children': [children],
                  'smoker': [smoker], 'region': [region]}

data_entry_table = pd.DataFrame(pretty_results)

## Google Sheet Version
df = data_entry_table.copy()
df['entry_date'] = entry_dir

## Update the Google Sheet
update_sheet(client)

st.caption("Data Entry Table")
st.table(data_entry_table)