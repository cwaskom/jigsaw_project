import os
import pytest
from run_adapters import hotel_ids_str

# Production Test - Tests the CSV of hotels to call from the API is properly opened and the Amadeus ID's are converted to a string to prepare for API call
# If add more hotels than Aman, update the hotel_ids str below:
hotel_ids = 'AMATHAAZ,AMBJVARU,AMCMBAAW,AMCMBAMA,AMCVFAAL,AMDPSAKA,AMDPSAMI,AMHGHAFA,AMHKTAMP,AMJACAMG,AMJAIAAK,AMJAIAMA,AMJOGABA,AMLJGAMA,AMLPQAAT,AMMNLAMP,AMNGOAMA,AMNHAAOI,AMPEKASP,AMPGAAGI,AMPLSAAY,AMPOPAME,AMQBAAAS,AMRAKTAH,AMREPASA,AMSHAAMN,AMSWQAWA,AMTYOATK,AMVCECGV,AMDPSASN,AMUKYANK'

hotel_csv = 'hotel_list_prod.csv'

def test_hotel_ids_prod():
    hotel_id_str = hotel_ids_str(hotel_csv)  ### FIX: NOT RECOGNIZING STRING
    assert hotel_id_str == hotel_ids