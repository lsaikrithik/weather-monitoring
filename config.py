import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY') 
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')

TEMP_THRESHOLD = 35.0  
ALERT_CONSECUTIVE_COUNT = 2 

POLL_INTERVAL = 300
