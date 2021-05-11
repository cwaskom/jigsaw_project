import psycopg2
import pytest

import api.src.adapters as adapters
import api.src.db.db as db
import api.src.models as models
from .test_adapters import json

from settings import (DBTEST_NAME, DBTEST_USER, DBTEST_PASSWORD)

@pytest.fixture(scope = 'module')
def test_conn():
    test_conn = psycopg2.connect(dbname=DBTEST_NAME, user=DBTEST_USER, password=DBTEST_PASSWORD)
    cursor = test_conn.cursor()
    db.drop_all_tables(test_conn, cursor)
    # db.reset_all_primarykey(test_conn, cursor)
    yield test_conn
    db.drop_all_tables(test_conn, cursor)
    # db.reset_all_primarykey(test_conn, cursor)

def test_inserted_data(test_conn):
    test_cursor = test_conn.cursor()
    builder = adapters.HotelBuilder()
    builder_details = builder.select_attributes(json)
    hotel = db.save(builder_details, test_conn, test_cursor)
    
    hotel_data = db.find(models.Hotel, hotel.id, test_cursor)
    assert hotel_data.name == 'BULGARI HOTELS RESORTS MILANO'


