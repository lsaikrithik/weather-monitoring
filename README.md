# Weather Monitoring System

## Objective
Develop a real-time data processing system to monitor weather conditions and provide summarized insights using rollups and aggregates. The system utilizes data from the OpenWeatherMap API.

## Table of Contents
1. [Features](#features)
2. [Technologies](#technologies)
3. [Codebase Structure](#codebase-structure)
4. [Design Choices](#design-choices)
5. [Dependencies](#dependencies)
6. [Setup Instructions](#setup-instructions)
7. [Conclusion](#conclusion)

## Features
- Fetch real-time weather data for multiple cities.
- Store weather data in a MongoDB database.
- Provide daily summaries of weather conditions.
- Generate alerts based on specified thresholds (e.g., high temperatures).
- Web interface to view summaries and alerts.

## Technologies
- **Backend:** Flask (Python)
- **Database:** MongoDB
- **Weather Data API:** OpenWeatherMap API
- **Frontend:** HTML/CSS (served via Flask)

## Codebase Structure
weather-monitoring/ 

│ 

├── app.py # Main application file 

├── config.py # Configuration file for API keys and DB settings 

├── weather.py # Weather data fetching and processing logic 

├── templates/ # HTML templates for the web interface 

│     └── home.html # Main page template 

├── static/ # Static files (e.g., images) 

|      └── weather.jpg # Background image for the web interface 

└── .env # Environment variables (API keys, DB URI)

## Design Choices

### Data Fetching and Storage:
- The application fetches weather data for multiple cities using the OpenWeatherMap API.
- Weather data is stored in a MongoDB database, allowing for efficient querying and aggregation of data.

### Background Data Polling:
- A separate thread is used to poll weather data at specified intervals (5 minutes by default) without blocking the main application.
- Alerts are generated based on consecutive high temperatures, stored in the database, and displayed on the web interface.

### Daily Summary Generation:
- The application provides daily summaries for each city, calculating average, maximum, and minimum temperatures using MongoDB's aggregation framework.

### Responsive Alerts System:
- Alerts are displayed on the main page, allowing users to mark them as read.

### Separation of Concerns:
- The application is structured to separate configuration, fetching logic, and web interface, making it easier to maintain and extend.

## Dependencies
To run the application, ensure you have the following dependencies installed:
- Flask
- Flask-PyMongo
- requests
- python-dotenv
- pytz

## Setup Instructions

### Prerequisites
- Install Docker.

### Running the Application

#### Clone the Repository

```bash
git clone https://github.com/yourusername/rule_engine.git
cd rule_engine
```

Build and Run with Docker
- To build and run the application, execute the following command:

```bash
docker-compose build
docker-compose up
```

### Access the Application
- Open your web browser and go to http://localhost:5000 to access the Weather Monitoring System application.

## Conclusion
- The Weather Monitoring System is a robust application designed to provide real-time weather data and insights using the OpenWeatherMap API. Leveraging Flask for the backend and MongoDB for data storage, this system fetches, processes, and displays weather information while generating alerts based on predefined thresholds.

- By utilizing Docker, the application ensures consistent performance across different environments, simplifying deployment and maintenance. The comprehensive documentation included in this README facilitates easy setup and understanding of the system's architecture and functionalities.


