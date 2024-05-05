import streamlit as st
import pandas as pd

# Display a message
st.title("Metrics Filterer")
st.write("Choose an option!")

country_locs = pd.read_csv("countries_locations.csv")
country_metrics = pd.read_csv("country_data.csv")
country_metrics.rename(columns={'Country': 'name'}, inplace=True)

merged_countries = pd.merge(country_locs, country_metrics, on='name', how='left').drop_duplicates(subset=['name']).dropna().drop(columns=["country"])
columns_to_move = ['latitude', 'longitude']
merged_countries = merged_countries[[col for col in merged_countries.columns if col not in columns_to_move] + columns_to_move]

# Display options
st.write('1. Filter by country')
st.write('2. Filter by metric')

# Get user input
user_input = st.text_input('Please input a number corresponding to any of the options above')

# Handle user input
if user_input.strip() == '':
    st.write("Please input a valid number.")
else:
    user_input = int(user_input)

    # Filter by country
    if user_input == 1:
        # Display country list
        country_choice = st.selectbox('Please pick a country:', merged_countries['name'])
        if country_choice:
            # Display country details
            country_data = merged_countries[merged_countries['name'] == country_choice].iloc[0]
            st.write(f'Chosen country: {country_choice}')
            st.write(f'Happiness Score: {country_data["HappinessScore"]}')
            st.write(f'GDPPC: {country_data["GDPPC"]}')
            st.write(f'Social Support: {country_data["SocialSupport"]}')
            st.write(f'Life Expectancy: {country_data["LifeExpectancy"]}')
            st.write(f'Freedom: {country_data["Freedom"]}')
            st.write(f'Government Corruption: {country_data["GovernmentCorruption"]}')
            st.write(f'Generosity: {country_data["Generosity"]}')

    # Filter by metric
    elif user_input == 2:
        # Display metric options
        st.write('1. Happiness Score')
        st.write('2. GDPPC')
        st.write('3. Social Support')
        st.write('4. Life Expectancy')
        st.write('5. Freedom')
        st.write('6. Government Corruption')
        st.write('7. Generosity')

        # Get user input for metric
        metric_input = st.text_input('Please select a metric:', key='metric_input')

        if metric_input.strip() == '':
            st.write("Please input a valid number.")
        else:
            metric_input = int(metric_input)

            # Display top and bottom countries based on selected metric
            if metric_input in range(1, 8):
                metric_name = merged_countries.columns[metric_input + 1]
                sorted_countries = merged_countries.sort_values(by=metric_name, ascending=False)
                st.write("The top five countries:")
                st.write(sorted_countries[['name', metric_name]].head())
                st.write("The bottom five countries:")
                st.write(sorted_countries[['name', metric_name]].tail())
            else:
                st.write("Invalid metric number. Please input a number between 1 and 7.")
