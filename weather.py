import requests
from datetime import datetime
from pymongo import MongoClient
from config import API_KEY, BASE_URL, CITIES, MONGO_URI, DB_NAME, TEMP_THRESHOLD, ALERT_CONSECUTIVE_COUNT

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def fetch_weather(city):
    params = {'q': city, 'appid': API_KEY}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'city': city,
            'temp': kelvin_to_celsius(data['main']['temp']),
            'max_temp': kelvin_to_celsius(data['main']['temp_max']),
            'min_temp': kelvin_to_celsius(data['main']['temp_min']),
            'weather': data['weather'][0]['main'],
            'timestamp': datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        print(f"Error fetching weather data for {city}: {response.status_code}, {response.text}")
    return None

def store_weather_data(data):
    db.weather_data.insert_one(data)

def get_daily_summary(city, date):
    pipeline = [
        {"$match": {
            "city": city,
            "timestamp": {
                "$gte": f"{date} 00:00:00", 
                "$lt": f"{date} 23:59:59"   
            }
        }},
        {"$group": {
            "_id": "$city",
            "avg_temp": {"$avg": "$temp"},
            "max_temp": {"$max": "$max_temp"},
            "min_temp": {"$min": "$min_temp"},
            "dominant_weather": {"$first": "$weather"}
        }}
    ]
    result = list(db.weather_data.aggregate(pipeline))
    if result:
        return {
            "_id": result[0]["_id"],
            "avg_temp": round(result[0]["avg_temp"], 2), 
            "max_temp": round(result[0]["max_temp"], 2), 
            "min_temp": round(result[0]["min_temp"], 2),  
            "dominant_weather": result[0]["dominant_weather"]
        }
    
    return {
        "_id": city,
        "avg_temp": 0,
        "max_temp": 0,
        "min_temp": 0,
        "dominant_weather": "N/A"
    }

def check_alerts(city):
    recent_data = list(db.weather_data.find({"city": city}).sort("timestamp", -1).limit(ALERT_CONSECUTIVE_COUNT))
    if len(recent_data) < ALERT_CONSECUTIVE_COUNT:
        return None
    
    consecutive_high = all(data['temp'] > TEMP_THRESHOLD for data in recent_data)
    if consecutive_high:
        return f"Consecutive high temperatures recorded for {city}!"

    return None
