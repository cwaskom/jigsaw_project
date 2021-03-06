import psycopg2
import api.src.models as models
import api.src.db as db
import api.src.adapters as adapters


class Builder:
    def run(self, hotel_details, conn, cursor):
        amadeus_id = hotel_details['hotel']['hotelId']
        hotel_obj = db.find_by_amadeus_id(models.Hotel, amadeus_id, cursor)
        if hotel_obj:
            hotel_obj.exists = True
            offer = OfferBuilder().run(hotel_details, hotel_obj, conn, cursor)
            offer.hotel_id = hotel_obj.id
            saved_offer = db.save(offer, conn, cursor)
            print(saved_offer.__dict__)
            return {'hotel': hotel_obj, 'location': hotel_obj.location_id, 'offer': saved_offer} # LOCATION METHOD - RELATIONSHIP QUERY METHOD

        else:
            # run location, save location
            location = LocationBuilder().run(hotel_details, conn, cursor) # This is returning a dict but save needs an obj
            saved_location = db.save(location, conn, cursor)
            # run hotel, load in location, save hotel
            hotel = HotelBuilder().run(hotel_details, saved_location, conn, cursor)
            hotel.location_id = saved_location.id
            saved_hotel = db.save(hotel, conn, cursor)
            # run offer, load in hotel, save offer
            offer = OfferBuilder().run(hotel_details, saved_hotel, conn, cursor)
            offer.hotel_id = saved_hotel.id
            saved_offer = db.save(offer, conn, cursor)
            return {'hotel': saved_hotel, 'location': saved_location, 'offer': saved_offer}

class HotelBuilder:
    attributes = ['amadeus_id', 'name', 'chain_id', 'rating'] #location_id', 

    def select_attributes(self, hotel_details):
        amadeus_id = hotel_details['hotel']['hotelId']
        name = hotel_details['hotel']['name']
        chain_id = hotel_details['hotel']['chainCode']
        rating = hotel_details['hotel']['rating']
        return dict(zip(self.attributes, [amadeus_id, name, chain_id, rating]))

    def run(self, hotel_details, location, conn, cursor):
        selected = self.select_attributes(hotel_details)
        amadeus_id = selected['amadeus_id']
        hotel = models.Hotel.find_by_amadeus_id(amadeus_id, cursor)
        if hotel:
            hotel.exists = True
            return hotel
        else:
            hotel_obj = models.Hotel(**selected)
            # hotel_obj.exists = False
            return hotel_obj

class LocationBuilder:
    attributes = ['lon', 'lat', 'address', 'city_name', 'postal_code', 'country_code']

    def select_attributes(self, hotel_details):
        lon = hotel_details['hotel']['longitude']
        lat = hotel_details['hotel']['latitude']
        address = hotel_details['hotel']['address']['lines'][0]
        city_name = hotel_details['hotel']['address']['cityName']
        postal_code = hotel_details['hotel']['address'].get('postalCode')
        country_code = hotel_details['hotel']['address']['countryCode']
        return dict(zip(self.attributes, [lon, lat, address, city_name, postal_code, country_code]))

    def run(self, hotel_details, conn, cursor):
        selected = self.select_attributes(hotel_details)
        location = models.Location(**selected)
        return location

class OfferBuilder:
    attributes = ['offer_id', 'check_in', 'check_out', 'available', 'currency', 'total_rate', 'comm_percentage']

    def select_attributes(self, hotel_details):
        offer_id = hotel_details['offers'][0]['id']
        check_in = hotel_details['offers'][0]['checkInDate']
        check_out = hotel_details['offers'][0]['checkOutDate']
        available = hotel_details['available']
        currency = hotel_details['offers'][0]['price']['currency']
        total_rate = hotel_details['offers'][0]['price']['total']
        comm_percentage = None
        return dict(zip(self.attributes, [offer_id, check_in, check_out, available, currency, total_rate, comm_percentage]))

    def run(self, hotel_details, hotel, conn, cursor):
        selected = self.select_attributes(hotel_details)
        offer = models.Offer(**selected)
        return offer

# class ChainBuilder:
#     attributes = ['chain_code', 'name']

#     def select_attributes(self, hotel_details):
#         chain_code, name = 
#         return categories

#     def run(self, venue_details, venue, conn, cursor):
#         category_names = self.select_attributes(venue_details)
#         categories = self.find_or_create_categories(category_names, conn, cursor)
#         venue_categories = self.create_venue_categories(venue, categories, conn, cursor)
#         return venue_categories