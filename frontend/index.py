import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from view_functions import (hotels_info, hotel_table_data, cheapest_by_hotel)

# Top of Body - Map of Aman Hotels
st.header('Aman Hotels Map')
data = pd.DataFrame(hotels_info())
st.map(data)

# NEEDS TO BE FIXED
px.set_mapbox_access_token(open(".mapbox_token").read())
df = px.data.hotels_info()
fig = px.scatter_mapbox(df, lat="lat", lon="lon")
fig.show()

# Middle of Body - Chart showing all of the hotels and their discounts
st.header('Cheapest Rate vs. Average Rate (% Discount)')
st.write('The U.S. hotels have higher average rates which makes the % discounts greater for the cheapest nights')
hotel_data = hotel_table_data()
hotel_names = [hotel["hotel"] for hotel in hotel_data]
percent_discount = [hotel["percent_discount"] for hotel in hotel_data if hotel["percent_discount"] != 0]
bar = go.Bar(x = hotel_names, y = percent_discount)
fig = go.Figure(bar)
st.plotly_chart(fig)


# Middle of Body - Dropdown box that when selected will return the cheapest dates
st.header ('Find The Cheapest Days (by Hotel)')
selected_hotel = st.selectbox('Select Hotel', [hotel['hotel'] for hotel in hotel_data]) 
cheapest_dates = cheapest_by_hotel(selected_hotel)
for date in cheapest_dates:
    check_in = date["check_in"]
    rate = date["rate"]
    currency = date["currency"]
    output = f"Check In: {check_in}         Total Rate (inc. Tax): {rate} {currency}" 
    st.write(output)