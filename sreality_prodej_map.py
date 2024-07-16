import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")

new_name = st.text_input("Enter a new name:")
new_pet = st.text_input("Enter a pet type:")

if st.button("Add to Spreadsheet"):
    # Create a new DataFrame for the new data
    new_data = {'name': new_name, 'pet': new_pet}
    df = df.append(new_data, ignore_index=True)

    # Write the updated DataFrame back to the Google Sheet
    conn.write(df)

    st.success("Data added successfully!")