import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


all_df = pd.read_csv("dashboard/main_data.csv")
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]


st.header('Bike Sharing Dashboard :bike:')
col1, col2 = st.columns(2)

st.subheader('Hourly Orders')
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df.cnt.sum()
    st.metric("Total rental", value=total_rentals)

with col2:
    best_hour = main_df.groupby(by="hr")['cnt'].sum().idxmax()
    st.metric("Best Hour", value=best_hour)

with col3:
    worst_hour = main_df.groupby(by="hr")['cnt'].sum().idxmin()
    st.metric("Worst Hour", value=worst_hour)

hourly_counts = main_df.groupby(by="hr")['cnt'].sum().sort_values(ascending=False).reset_index()
byhour_df = hourly_counts.sort_values(by="cnt", ascending=False).reset_index(drop=True).head(24)

byhour_df = byhour_df.sort_values(by="hr")

plt.figure(figsize=(24, 10))
plt.plot(
    byhour_df["hr"],
    byhour_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#72BCD4"
)
plt.title("Total Bike Rent by Hour", loc="center", fontsize=40)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Hour of the Day', fontsize=30)
plt.ylabel('Total Rented Bikes', fontsize=30)
plt.grid(True)
st.pyplot(plt)

st.subheader('Percentage of Customers by Weather Situation')
col1, col2 = st.columns(2)
weather_mapping = {
    1: "clear",
    2: "cloudy",
    3: "light rain",
    4: "heavy rain"
}
weather_counts = main_df.groupby(by="weathersit")['cnt'].sum()
weather_counts.index = weather_counts.index.map(weather_mapping)

with col1:
    best_weather = weather_counts.idxmax()
    st.metric("Best Weather", value=best_weather)

with col2:
    worst_weather = weather_counts.idxmin()
    st.metric("Worst Weather", value=worst_weather)


byweathersit_df = main_df.groupby(by="weathersit")['cnt'].sum().sort_values(ascending=False).reset_index()

byweathersit_df['weathersit'] = byweathersit_df['weathersit'].map(weather_mapping)

counts = byweathersit_df.sort_values(by="cnt", ascending=False)
labels = counts['weathersit']
sizes = counts['cnt']
colors = ["#DFF5FF", "#67C6E3", "#378CE7", "#5356FF"]
explode = (0.02, 0, 0.1, 0.1)

plt.figure(figsize=(10, 7))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, wedgeprops={'edgecolor' : 'black'}, explode=explode)
plt.title("Percentage of Customers by Weather Situation", fontsize=15)
plt.axis('equal')
st.pyplot(plt)