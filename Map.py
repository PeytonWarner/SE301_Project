import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

country_locs = pd.read_csv("countries_locations.csv")
country_metrics = pd.read_csv("country_data.csv")
country_metrics.rename(columns={'Country': 'name'}, inplace=True)

merged_countries = pd.merge(country_locs, country_metrics, on='name', how='left').drop_duplicates(subset=['name']).dropna().drop(columns=["country"])
columns_to_move = ['latitude', 'longitude']
merged_countries = merged_countries[[col for col in merged_countries.columns if col not in columns_to_move] + columns_to_move]

st.title("Country Analysis Map")
st.markdown("**Click on the markers to find the coordinates and metrics of different countries!**")
st.write("Type or use the dropdown box to easily locate a country!")

# Dropdown menu to select a country
selected_country = st.selectbox("Select a country", merged_countries['name'])

# Create a folium map
f = folium.Figure(width=1000, height=400)
m = folium.Map(location=[merged_countries['latitude'].mean(), merged_countries['longitude'].mean()], zoom_start=1.5).add_to(f)

# Add markers for each country
for i, row in merged_countries.iterrows():
    popup_text = f"<u><b><span style='font-size:12px'>{row['name']}</b></u></span><br>" \
                 f"<span style='white-space: nowrap'><b>Latitude:</b> {row['latitude']}</span><br>" \
                 f"<span style='white-space: nowrap'><b>Longitude:</b> {row['longitude']}</span><br>" \
                 f"<span style='white-space: nowrap'><b>Happiness Score:</b> {row['HappinessScore']}</span><br>" \
                 f"<span style='white-space: nowrap'><b>GDPPC:</b> {row['GDPPC']}</span><br>" \
                 f"<span style='white-space: nowrap'><b>Social Support:</b> {row['SocialSupport']}</span><br>" \
                 f"<span style='white-space: nowrap'><b>Life Expectancy:</b> {row['LifeExpectancy']}</span><br>" \
                 f"<span style='white-space: nowrap'><b>Freedom:</b> {row['Freedom']}</span><br>" \
                 f"<span style='white-space: nowrap'><b>Government Corruption:</b> {row['GovernmentCorruption']}</span><br>" \
                 f"<span style='white-space: nowrap'><b>Generosity:</span></b> {row['Generosity']}"
    
    # Add circle marker for each country
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=3, 
                        fill='blue', 
                        color='blue', 
                        opacity=0.5,
                        popup = popup_text
                        ).add_to(m)

# Highlight the selected country on the map
if selected_country:
    select_df = merged_countries[merged_countries['name'] == selected_country]
    red_marker_popup_text = f"<u><b><span style='font-size:12px'>{select_df['name'].values[0]}</b></u></span><br>" \
                            f"<span style='white-space: nowrap'><b>Latitude:</b> {select_df['latitude'].values[0]}</span><br>" \
                            f"<span style='white-space: nowrap'><b>Longitude:</b> {select_df['longitude'].values[0]}</span><br>" \
                            f"<span style='white-space: nowrap'><b>Happiness Score:</b> {select_df['HappinessScore'].values[0]}</span><br>" \
                            f"<span style='white-space: nowrap'><b>GDPPC:</b> {select_df['GDPPC'].values[0]}</span><br>" \
                            f"<span style='white-space: nowrap'><b>Social Support:</b> {select_df['SocialSupport'].values[0]}</span><br>" \
                            f"<span style='white-space: nowrap'><b>Life Expectancy:</b> {select_df['LifeExpectancy'].values[0]}</span><br>" \
                            f"<span style='white-space: nowrap'><b>Freedom:</b> {select_df['Freedom'].values[0]}</span><br>" \
                            f"<span style='white-space: nowrap'><b>Government Corruption:</b> {select_df['GovernmentCorruption'].values[0]}</span><br>" \
                            f"<span style='white-space: nowrap'><b>Generosity:</b> {select_df['Generosity'].values[0]}</span>"
    
    folium.Marker(location=[select_df['latitude'].values[0], select_df['longitude'].values[0]],
                  popup = red_marker_popup_text,
                  icon = folium.Icon(color='red', icon='info-sign')).add_to(m)

# Render the folium map
folium_static(m)


