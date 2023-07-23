import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static


@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


def main():
    st.title('Nepali Restaurants')
    st.subheader('around the world - v.0.9')

    # Load the CSV file
    file_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQQ2hZ4esuck1Z4nqgNmU27X-2U4rkixcho5SmzDOukGSltVxbQNqnJzUeHKJdRY_mf0e8cH0f_Z0OQ/pub?gid=1677561077&single=true&output=csv'
    df = load_data(file_path)
    
    # Create a dropdown menu for selecting countries
    countries = ['Select All'] + sorted(list(df['country'].unique()))
    
    
    # Create a dropdown menu for selecting countries
    selected_country = st.sidebar.selectbox('Select Country', countries)

    # Filter the DataFrame based on the selected country
    if selected_country == 'Select All':
        filtered_df = df  # Show all items if 'Select All' is chosen
    else:
        filtered_df = df[df['country'] == selected_country]

    # Filter the DataFrame based on the selected country
    # filtered_df = df[df['country'] == selected_country]


    # Create a folium map centered at the first location in the dataset
    map_center = [30,30]
    my_map = folium.Map(location=map_center, zoom_start=2, tiles='cartodbpositron')

    # Create a MarkerCluster layer for the map
    marker_cluster = MarkerCluster().add_to(my_map)

    # Add markers for each restaurant location in the DataFrame
    for index, row in filtered_df.iterrows():
        restaurant_name = row['restaurant_name']
        address = row['address']
        latitude = row['Latitude']
        longitude = row['Longitude']
        status = row['status']

        popup_text = f"<b>{restaurant_name}</b><br>{address}<br>{status}"

        folium.Marker(
            location=[latitude, longitude],
            popup=popup_text,
            icon=folium.Icon(color='blue', icon='cutlery', prefix='fa')
        ).add_to(marker_cluster)

    # Display the map using Streamlit
    folium_static(my_map,  width=800, height=600)

if __name__ == '__main__':
    main()
