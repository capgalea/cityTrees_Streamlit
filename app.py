import pandas as pd
import geopandas as gpd
import requests
import csv
import io
from shapely.geometry import Point
import streamlit as st

# URL of the dataset
url = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/trees-with-species-and-dimensions-urban-forest/records?select=common_name%2C%20diameter_breast_height%2C%20date_planted%2C%20latitude%2C%20longitude%2C%20age_description&limit=10&offset=0&timezone=UTC&include_links=false&include_app_metas=false"

# Send GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    
    # Decode the content to a string
    content = response.content.decode('utf-8')
    
    # Use io.StringIO to treat the string as a file
    csv_file = io.StringIO(content)
    
    # Read the CSV content
    csv_reader = csv.reader(csv_file, delimiter=';')
    
    # Write the CSV content to a properly formatted CSV file
    with open("trees_with_species_and_dimensions.csv", "w", newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        for row in csv_reader:
            csv_writer.writerow(row)
    
    print("Trees CSV file has been saved successfully.")
else:
    print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")

# # URL of the dataset
# url2 = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/microclimate-sensors-data/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true"

# # Send GET request
# response2 = requests.get(url2)

# # Check if the request was successful
# if response2.status_code == 200:
#     # Decode the content to a string
#     content2 = response2.content.decode('utf-8')
    
#     # Use io.StringIO to treat the string as a file
#     csv_file2 = io.StringIO(content2)
    
#     # Read the CSV content
#     csv_reader2 = csv.reader(csv_file2, delimiter=';')
    
#     # Write the CSV content to a properly formatted CSV file
#     with open("temp_envir.csv", "w", newline='', encoding='utf-8') as file:
#         csv_writer2 = csv.writer(file)
#         for row in csv_reader2:
#             csv_writer2.writerow(row)
    
#     print("Temp CSV file has been saved successfully.")
# else:
#     print(f"Failed to retrieve data. HTTP Status code: {response2.status_code}")

# # Load the datasets
# trees = pd.read_csv('trees_with_species_and_dimensions.csv', delimiter=';')
# temp = pd.read_csv('temp_envir.csv', delimiter=';')

# # Print the columns of the DataFrame
# print("Columns in the trees DataFrame:", trees.columns)
# print("Columns in the temp DataFrame:", temp.columns)

# dfTrees = pd.DataFrame(trees, columns=['Tree ID', 'Common Name', 'Date planted', 'Latitude', 'Longitude'])
# dfTemp = pd.DataFrame(temp, columns=['ID', 'Date', 'Location', 'LatLong', 'Min Wind Dir', 'Av Wind Dir', 'Max Wind Dir', 'Min Wind Speed', 'Av Wind Speed', 'Gust Wind Speed', 'Air Temperature (C)', 'Relative Humidity (%)', 'Atmos Press', 'pm25', 'pm10', 'noise'])

# # Convert date columns to datetime if the column exists
# if 'Date planted' in trees.columns:
#     trees['Date planted'] = pd.to_datetime(trees['Date planted'])
# else:
#     print("Column 'Date planted' not found in the trees DataFrame.")

# # Print the columns of the temp DataFrame
# print("Columns in the temp DataFrame:", temp.columns)
# print(trees.head())

# # Convert 'Date' to datetime if the column exists
# if 'Date' in dfTemp.columns:
#     temp['Date'] = pd.to_datetime(temp['Date'])
# else:
#     print("Column 'Date' not found in the temp DataFrame.")

# # Streamlit code to download temperature data
# if st.sidebar.button('Download Temperature Data'):
#     st.sidebar.download_button(
#         label="Click here to download",
#         data=temp.to_csv(index=False).encode('utf-8'),
#         file_name='melbourne_temperature_data.csv',
#         mime='text/csv',
#     )