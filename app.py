from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from weather import fetch_weather, store_weather_data, get_daily_summary, check_alerts
import threading
import time
from config import CITIES, POLL_INTERVAL, MONGO_URI, DB_NAME
from datetime import datetime
from bson.objectid import ObjectId
import pytz  

app = Flask(__name__)

app.config["MONGO_URI"] = MONGO_URI + DB_NAME
mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def home():
    utc_now = datetime.now(pytz.utc)  
    date_str = utc_now.strftime('%Y-%m-%d')
    
    summaries = [get_daily_summary(city, date_str) for city in CITIES]

    print("Daily Summaries:", summaries)

    alerts = list(db.alerts.find({"is_active": True}).sort("timestamp", -1))

    db.alerts.update_many({"is_active": True}, {"$set": {"is_active": False}})
    
    return render_template('home.html', summaries=summaries, alerts=alerts)

@app.route('/mark_inactive/<alert_id>')
def mark_inactive(alert_id):
    db.alerts.update_one({"_id": ObjectId(alert_id)}, {"$set": {"is_active": False}})
    return redirect(url_for('home'))

def poll_weather_data():
    while True:
        for city in CITIES:
            weather_data = fetch_weather(city)
            if weather_data:
                store_weather_data(weather_data)
                alert = check_alerts(city)
                if alert:
                    print(alert)  
                    db.alerts.insert_one({
                        'city': city,
                        'alert': alert,
                        'timestamp': datetime.now(pytz.utc),  
                        'is_active': True 
                    })
        time.sleep(POLL_INTERVAL)  
        

if __name__ == '__main__':
    thread = threading.Thread(target=poll_weather_data)
    thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)
