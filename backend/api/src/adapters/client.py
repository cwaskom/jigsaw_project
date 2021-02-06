from amadeus import Client, ResponseError
import requests
from settings import CLIENT_ID, CLIENT_SECRET


# hotel_list = "BGMILBGB" #"BGMILBGB,BGLONBGB"

class HotelClient:
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET
    
    def __init__(self):
        self.amadeus = Client(client_id=HotelClient.CLIENT_ID, client_secret=HotelClient.CLIENT_SECRET, hostname='production')

    def request_offers(self, hotel_list, check_in_date, check_out_date):
        try:
            response = self.amadeus.shopping.hotel_offers.get(
                hotelIds=hotel_list, 
                checkInDate=check_in_date, 
                checkOutDate=check_out_date,
                bestRateOnly='true')
            return response.data
        except ResponseError as error:
            print(error) 