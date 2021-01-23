import api.src.db as db
import api.src.models as models

class Offer:
    __table__ = 'offers'
    columns = ['id', 'hotel_id', 'offer_id', 'check_in', 'check_out', 'available', 'currency', 'total_rate', 'comm_percentage', 'created_at']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    def hotel(self, cursor):
        hotel_query = """SELECT * FROM hotels WHERE hotel_id = %s"""
        cursor.execute(hotel_query, (self.hotel_id))
        record = cursor.fetchone()
        return db.build_from_record(models.Hotel, record)

    def find_cheapest_offer(self, cursor): #ORDER cheapest to most expensive
        cheapest_query = """SELECT * FROM offers WHERE hotel_id = %s ORDER BY total_rate ASC LIMIT 1"""
        cursor.execute(cheapest_query, (self.id))
        record = cursor.fetchone()
        return db.build_from_record(models.Offer, record)

    def find_average_offer(self, cursor):
        average_query = """SELECT AVG(total_rate) FROM offers WHERE hotel_id = %s"""
        cursor.execute(average_query, (self.id))
        record = cursor.fetchone()
        return db.build_from_record(models.Offer, record)

    def find_offers_by_date(self, cursor): # Do less than or between 
        average_query = """SELECT DATE_TRUNC('day',check_in) FROM offers WHERE cre'%s';"""
        cursor.execute(average_query, (self.id)) # need to 
        record = cursor.fetchone()
        return db.build_from_record(models.Offer, record)

    @classmethod
    def search(self, cursor):
        return db.find_all(Offer, cursor)
        