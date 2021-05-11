import pytest
import psycopg2
from datetime import date, timedelta
import api.src.adapters as adapters
import api.src.db.db as db
import api.src.models as models

def test_client_response():
    # check Bulgari Hotel Milan with search 
    hotel = adapters.HotelClient()
    response = hotel.amadeus.shopping.hotel_offers.get(
                    hotelIds="BGMILBGB", # TILONRHO,BGMILBGB,BGLONBGB
                    bestRateOnly='true')
    assert response.status_code == 200

def test_client_dates_search():
    # Checks date input feature works with datetime
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    hotel = adapters.HotelClient()
    response = hotel.request_offers(hotel_list="BGMILBGB", check_in_date=check_in, check_out_date=check_out)
    assert response[0]['hotel']['name'] == "Bulgari Hotel Milano"

def test_client_returns_location():
    # checks the response has a location value
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    hotel = adapters.HotelClient()
    response = hotel.request_offers(hotel_list="BGMILBGB", check_in_date=check_in, check_out_date=check_out)
    assert response[0]['hotel']['address']['lines'][0] == 'VIA PRIVATA FRATELLI GABBA 7B'