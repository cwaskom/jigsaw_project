import api.src.db as db
import api.src.models as models
import datetime

class Hotel:
    __table__ = 'hotels'
    columns = ['id', 'amadeus_id', 'name', 'location_id', 'chain_id', 'rating']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    

    # Returns the hotel's id, name, lon, late. Used in /hotels route
    @classmethod
    def hotel_locations(self, cursor):
        details_query = """SELECT hotels.id, hotels.name, locations.lon, locations.lat 
                            FROM hotels JOIN locations ON locations.id = hotels.location_id""" 
        cursor.execute(details_query)
        location_records = cursor.fetchall()
        return location_records

    # /hotels/cheapest: Returns the cheapest rate, average rate, and percent discount of the cheapest rate
    @classmethod 
    def min_avg_rate(self, cursor): 
        percent_disc_query = """SELECT hotels.name, offers.currency, MIN(offers.total_rate) as min_rate, 
                                ROUND(AVG(offers.total_rate),2) AS avg_rate,  
                                100*ROUND((MIN(offers.total_rate)/(AVG(offers.total_rate)))-1,2) AS percent_disc 
                            FROM offers JOIN hotels ON offers.hotel_id = hotels.id 
                            WHERE offers.created_at > %s
                            GROUP BY hotels.name, offers.currency
                            ORDER BY percent_disc ASC;"""
        time_24_hours_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        cursor.execute(percent_disc_query, (time_24_hours_ago, ))
        discount_records = cursor.fetchall()
        return discount_records

    # /hotels/cheapest/<name>: Uses the cheapest rate for a hotel and returns the dates that rate is available
    @classmethod
    def cheapest_dates(self, cursor, name, rate):
        cheapest_dates_query ="""SELECT hotels.name, offers.check_in, offers.currency, offers.total_rate, offers.created_at 
                                FROM offers JOIN hotels on offers.hotel_id = hotels.id 
                                WHERE offers.created_at > %s AND hotels.name = %s AND offers.total_rate = %s;"""
        time_24_hours_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        cursor.execute(cheapest_dates_query, (time_24_hours_ago, name, rate,))
        cheapest_dates_record = cursor.fetchall()
        return cheapest_dates_record

    # Searches the db for a hotel name and returns all of the availability from cheapest to most expensive
    @classmethod # could turn this into an instance method. first find hotel by the name, then call hotel.selected_rates
    def selected_hotel_rates(self, cursor, name): # Return the offer, ordered by total_rate ASC, where created_at , WHERE offers.hotel_id = self.id
        selected_hotel_rate_query = """SELECT hotels.name, offers.currency, offers.check_in, offers.total_rate, offers.created_at
                            FROM offers JOIN hotels ON offers.hotel_id = hotels.id 
                            WHERE hotels.name = %s AND offers.created_at > %s ORDER BY offers.total_rate ASC;""" 
        time_24_hours_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        cursor.execute(selected_hotel_rate_query, (name, time_24_hours_ago, ))
        selected_hotels = cursor.fetchall()
        return selected_hotels

    # Instance method that connects the offers table to the hotel table
    def offers(self, cursor):
        offers_query = """SELECT * FROM offers WHERE offers.hotel_id = %s AND offers.created_at > %s"""
        time_24_hours_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        cursor.execute(offers_query, (self.id, time_24_hours_ago,))
        records = cursor.fetchall()
        return db.build_from_records(models.Offer, records)

    # Instance method that connects the location table to the hotel table
    def location(self, cursor):
        location_query = """SELECT * FROM locations WHERE locations.id = %s"""
        cursor.execute(location_query, (self.location_id,))
        record = cursor.fetchone()
        return db.build_from_record(models.Location, record)

    # Takes a hotel object converts the attributes to dictionaries and adds the location and offers dictionaries.
    def to_json(self, cursor):
        offers = self.offers(cursor)
        location = self.location(cursor)
        hotel_dict = self.__dict__
        location_dict = location.__dict__
        offers_dicts = [offer.__dict__ for offer in offers]
        hotel_dict['location'] = location_dict
        hotel_dict['offers'] = offers_dicts
        return hotel_dict