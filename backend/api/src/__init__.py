from flask import Flask
from flask import request
import simplejson as json
from settings import DB_NAME, DEBUG, TESTING, DB_HOST, DB_USER, DB_PASSWORD

import api.src.db as db 
import api.src.models as models 

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=DB_NAME,
        DB_HOST=DB_HOST,
        DEBUG=DEBUG,
        TESTING=TESTING,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD  
    )

    @app.route('/')
    def root_url():
        return 'Welcome to the hotels API'
    
    @app.route('/hotels')
    def hotels():
        conn = db.get_db()
        cursor = conn.cursor()

        hotels_detail = models.Hotel.hotel_locations(cursor)
        details_dict = [dict(zip(['id', 'name', 'lon', 'lat'], hotel_detail)) for hotel_detail in hotels_detail]
        return json.dumps(details_dict, default=str)
    
    # Returns each hotel and the cheapest rate, average, rate, and percentage discount. Ordered by greatest discount to smallest discount.
    @app.route('/hotels/cheapest')
    def cheapest():
        conn = db.get_db()
        cursor = conn.cursor()
        hotel_rates_min_avg = models.Hotel.min_avg_rate(cursor)
        rate_min_avg_dict  = [dict(zip(['hotel', 'currency', 'cheapest', 'average', 'percent_discount'], hotel)) for hotel in hotel_rates_min_avg]
        return json.dumps(rate_min_avg_dict, default=str)

    # Returns an individual hotel with the cheapest rates and the dates those are available
    @app.route('/hotels/cheapest/<name>')
    def cheapest_by_name(name):
        conn = db.get_db()
        cursor = conn.cursor()

        hotel_rates_min_avg = models.Hotel.min_avg_rate(cursor)
        rate_min_avg_dict  = [dict(zip(['hotel', 'currency', 'cheapest', 'average', 'percent_discount'], hotel)) for hotel in hotel_rates_min_avg]
        name_cleaned = name.title()
        hotels = []
        for hotel in rate_min_avg_dict:
            if name_cleaned in hotel['hotel']:
                hotels.append(hotel)
        selected_name, selected_rate = hotels[0]["hotel"], hotels[0]["cheapest"]
        cheapest_dates = models.Hotel.cheapest_dates(cursor, selected_name, selected_rate)
        cheapest_dates_dict = [dict(zip(['hotel', 'check_in', 'currency', 'rate', 'created_at'], date)) for date in cheapest_dates]
        return json.dumps(cheapest_dates_dict, default=str)

    # Returns a hotel's availability ordered cheapest to most expensive
    @app.route('/hotels/<name>') 
    def select_hotel_by_name(name):
        conn = db.get_db()
        cursor = conn.cursor()
        cleaned_name = name.capitalize()

        selected_hotel_rates = models.Hotel.selected_hotel_rates(cursor, cleaned_name)
        hotel_rates_dict  = [dict(zip(['hotel', 'currency', 'check_in', 'rate', 'created_at'], hotel)) for hotel in selected_hotel_rates]
        return json.dumps(hotel_rates_dict, default=str)

    # Uses objects to pull records from the database, make instance method calls, and return data
    @app.route('/hotels/id/<id>')
    def search_offers(id):
        conn = db.get_db()
        cursor = conn.cursor()
        
        hotel = db.find(models.Hotel, id, cursor)        
        return json.dumps(hotel.to_json(cursor), default=str)

    return app


    # @app.route('/offers')
    # def offers():
    #     conn = db.get_db()
    #     cursor = conn.cursor()

    #     offers = db.find_all(models.Offer, cursor)
    #     offers_dicts = [offer.__dict__ for offer in offers]
    #     return json.dumps(offers_dicts, default=str)