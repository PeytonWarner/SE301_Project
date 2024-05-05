import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_bar_graphs(df, selected_countries, variable):
    plt.figure(figsize=(10, 6))
    for country in selected_countries:
        data = df[df['name'] == country][variable].squeeze()
        plt.bar(country, data, label=country)
        plt.text(country, data, str(data), ha='center', va='bottom')
    plt.xlabel('Countries')
    plt.ylabel(variable)
    plt.title(f'{variable} for Selected Countries')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()
    st.pyplot()

st.title("Country Metrics Visualizer")
st.write("Select up to 10 countries you would like to compare. Then, select the metric you would like to analyze.")

country_locs = pd.read_csv("countries_locations.csv")
country_metrics = pd.read_csv("country_data.csv")
country_metrics.rename(columns={'Country': 'name'}, inplace=True)

merged_countries = pd.merge(country_locs, country_metrics, on='name', how='left').drop_duplicates(subset=['name']).dropna().drop(columns=["country"])
columns_to_move = ['latitude', 'longitude']
merged_countries = merged_countries[[col for col in merged_countries.columns if col not in columns_to_move] + columns_to_move]

variables = merged_countries.columns[1:]

selected_countries = st.multiselect("Select countries:", merged_countries['name'])
selected_variable = st.selectbox("Select a Metric:", variables)

plot_bar_graphs(merged_countries, selected_countries, selected_variable)


