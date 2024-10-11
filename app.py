import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Set page configuration
st.set_page_config(layout="wide")

# Function to fetch data from API
@st.cache_data
def fetch_data(url):
    response = requests.get(url)
    data = response.json()
    if isinstance(data, list):
        return pd.json_normalize(data)
    else:
        raise TypeError("Expected JSON response to be a list")

# URLs for the datasets
trees_url = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/trees-with-species-and-dimensions-urban-forest/exports/json?select=common_name%2C%20diameter_breast_height%2C%20located_in%2C%20date_planted%2C%20age_description%2C%20latitude%2C%20longitude&where=%20date_planted%20%3E%202020-01-01&order_by=%20date_planted&limit=10000&timezone=UTC&use_labels=false&epsg=4326"
landmarks_url = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/landmarks-and-places-of-interest-including-schools-theatres-health-services-spor/exports/json?limit=10000&timezone=UTC&use_labels=false&epsg=4326"

# Fetch data
trees_data = fetch_data(trees_url)
landmarks_data = fetch_data(landmarks_url)

# Data preparation
trees_data['date_planted'] = pd.to_datetime(trees_data['date_planted'])
trees_data['month_planted'] = trees_data['date_planted'].dt.to_period('M').astype(str)

# Rename columns for better readability
trees_data.rename(columns={
    'common_name': 'Common Name',
    'diameter_breast_height': 'Diameter at Breast Height',
    'date_planted': 'Date Planted',
    'located_in': 'Located In',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'age_description': 'Age Description'
}, inplace=True)

landmarks_data.rename(columns={
    'feature_name': 'Feature Name',
    'theme': 'Theme',
    'sub_theme': 'Sub Theme',
    'co_ordinates.lat': 'Latitude',
    'co_ordinates.lon': 'Longitude'
}, inplace=True)

# Charts
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Melbourne</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-top: 0;'>Trees and Landmarks</h2>", unsafe_allow_html=True)

# Place multiselect and radio button side by side
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    selected_tree = st.multiselect('Select a tree:', trees_data['Common Name'].unique(), key='tree_multiselect')
with col2:
    chart_type = st.radio('Show Chart', ['Line', 'Bar'], key='chart_type_radio')
with col3:
    selected_landmarks = st.multiselect('Select a landmark:', landmarks_data['Theme'].unique(), key='landmark_multiselect')

# Number of trees planted per month as a scatter plot with lines
trees_per_month = trees_data.groupby(['month_planted', 'Common Name']).size().reset_index(name='count')

# Filter data based on selected trees
if selected_tree:
    filtered_trees_data = trees_data[trees_data['Common Name'].isin(selected_tree)]
    filtered_trees_per_month = trees_per_month[trees_per_month['Common Name'].isin(selected_tree)]
else:
    filtered_trees_data = trees_data
    filtered_trees_per_month = trees_per_month

# Create bar and line charts based on filtered data
fig_trees_bar = px.bar(filtered_trees_per_month, x='month_planted', y='count', title='Number of Trees Planted Per Month')
fig_trees_line = px.line(filtered_trees_per_month, x='month_planted', y='count', color='Common Name', title='Number of Trees Planted Per Month', markers=True)

# Select the chart type based on the radio button selection
if chart_type == 'Line':
    fig_trees = fig_trees_line
else:
    fig_trees = fig_trees_bar

# Number of each landmark type
landmarks_count = landmarks_data.groupby('Theme').size().reset_index(name='count')
fig_landmarks = px.bar(landmarks_count, x='count', y='Theme', title='Number of Each Landmark Type')

# Map showing locations of filtered trees and landmarks
fig_map1 = px.scatter_mapbox(filtered_trees_data, lat='Latitude', lon='Longitude', hover_data={'Common Name': True, 'Located In': True, 'Latitude': False, 'Longitude': False}, 
                            color='Common Name', color_discrete_sequence=px.colors.qualitative.Plotly, zoom=11.5, height=500, title='Tree Locations')

# Filter landmarks data based on selected landmarks
if selected_landmarks:
    filtered_landmarks_data = landmarks_data[landmarks_data['Theme'].isin(selected_landmarks)]
else:
    filtered_landmarks_data = landmarks_data

fig_map2 = px.scatter_mapbox(filtered_landmarks_data, lat='Latitude', lon='Longitude', color = 'Theme', hover_data={'Feature Name': True, 'Theme': True, 'Sub Theme': True, 'Latitude': False, 'Longitude': False},
                            color_discrete_sequence=px.colors.qualitative.Plotly, zoom=11.5, height=500, title='Landmark Locations')

# Update layout for title and legend
fig_map1.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0},
    title="Tree Locations",
    legend=dict(
        title="Legend",
        itemsizing='constant'
    )
)

fig_map2.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0},
    title="Landmark Locations",
    legend=dict(
        title="Legend",
        itemsizing='constant'
    )
)

# Display charts side by side
col1, col2 = st.columns(2)
col1.plotly_chart(fig_trees, use_container_width=True)
col2.plotly_chart(fig_landmarks, use_container_width=True)

# Limit the width of the map
map_col1, map_col2 = st.columns([2, 2])
with map_col1:
    st.plotly_chart(fig_map1, use_container_width=True)
with map_col2:
    st.plotly_chart(fig_map2, use_container_width=True)

# Display data tables at the bottom of the page
col1, col2 = st.columns([2, 2])
with col1:
    st.subheader("Trees Data Table")
    st.dataframe(filtered_trees_data, height=300)
with col2:
    st.subheader("Landmarks Data Table")
    st.dataframe(filtered_landmarks_data, height=300)
