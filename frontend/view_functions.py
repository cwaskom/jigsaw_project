import requests
HOTEL_INFO_URL = "http://127.0.0.1:5000/hotels"
HOTEL_RATES_PERC_DISC = "http://127.0.0.1:5000/hotels/cheapest"


def hotels_info():
    response = requests.get(HOTEL_INFO_URL)
    return response.json()

def hotel_table_data():
    response = requests.get(HOTEL_RATES_PERC_DISC)
    return response.json()

def cheapest_by_hotel(name):
    response = requests.get(f"http://127.0.0.1:5000/hotels/cheapest/{name}")
    return response.json()

# def find_hotel_by_id(id):
#     # response = requests.get(API_URL, params={'name': hotel_name})
#     response = requests.get(f"{API_URL}/{id}")
#     return response.json()
