import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DEBUG = True
TESTING = True

DBTEST_NAME = os.getenv("DBTEST_NAME")
DBTEST_USER = os.getenv("DBTEST_USER")
DBTEST_PASSWORD = os.getenv("DBTEST_PASSWORD")
DBTEST_HOST = os.getenv("DBTEST_HOST")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")