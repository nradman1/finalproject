import requests
from datetime import datetime, timedelta
from config import YELP_API_KEY, TICKETMASTER_API_KEY, AMC_API_KEY, GOOGLE_MAPS_API_KEY

# API Keys - Replace with your actual keys


# Function to calculate distance between two sets of coordinates using Google Maps Distance Matrix API
def calculate_distance(api_key, origin_coords, destination_coords):
    maps_endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "key": api_key,
        "origins": f"{origin_coords[0]},{origin_coords[1]}",
        "destinations": f"{destination_coords[0]},{destination_coords[1]}",
    }

    response = requests.get(maps_endpoint, params=params)
    data = response.json()
    distance = data["rows"][0]["elements"][0]["distance"]["text"]

    return distance

# Function to get Yelp recommendations based on user inputs
def get_yelp_recommendations(api_key, cuisine, dietary_restriction, date, location, travel_distance):
    # Use Yelp Fusion API to search for restaurants
    yelp_endpoint = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "term": cuisine,
        "limit": 3,
        "location": location,
    }

    response = requests.get(yelp_endpoint, headers=headers, params=params)
    data = response.json()

    # Extract and return relevant information from the Yelp response
    recommendations = []
    for business in data.get("businesses", []):
        recommendations.append({
            "name": business["name"],
            "address": business["location"]["address1"],
            "distance": calculate_distance(GOOGLE_MAPS_API_KEY, [business["coordinates"]["latitude"], business["coordinates"]["longitude"]], location),
            "rating": business["rating"],
            "price": business.get("price", "Not available"),
        })

    return recommendations

# Function to get Ticketmaster event recommendations based on user inputs
def get_ticketmaster_events(api_key, date, location, travel_distance):
    # Use Ticketmaster API to search for events
    ticketmaster_endpoint = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": api_key,
        "startDateTime": f"{date}T00:00:00",
        "endDateTime": f"{date}T23:59:59",
        "city": location,
        "size": 3,
    }

    response = requests.get(ticketmaster_endpoint, params=params)
    data = response.json()

    # Extract and return relevant information from the Ticketmaster response
    recommendations = []
    for event in data.get("_embedded", {}).get("events", []):
        recommendations.append({
            "name": event["name"],
            "venue": event["_embedded"]["venues"][0]["name"],
            "date": event["dates"]["start"]["local"],
            "distance": calculate_distance(GOOGLE_MAPS_API_KEY, [event["_embedded"]["venues"][0]["location"]["latitude"], event["_embedded"]["venues"][0]["location"]["longitude"]], location),
        })

    return recommendations

# Function to get AMC movie recommendations based on user input
def get_amc_movies(api_key, genre, location, travel_distance):
    # Use AMC Movies API to search for movies
    amc_endpoint = "https://api.amctheatres.com/v2/movies"
    headers = {"Api-Key": api_key}
    params = {"filter": f"genre eq '{genre}'", "top": 3, "lat": location.split(',')[0], "lon": location.split(',')[1]}

    response = requests.get(amc_endpoint, headers=headers, params=params)
    data = response.json()

    # Extract and return relevant information from the AMC Movies response
    recommendations = []
    for movie in data.get("data", []):
        recommendations.append({
            "title": movie["attributes"]["title"],
            "release_date": movie["attributes"]["releaseDate"],
            "rating": movie["attributes"]["rating"],
            "theatre": f"{movie['attributes']['theatre']['name']} ({calculate_distance(GOOGLE_MAPS_API_KEY, [movie['attributes']['theatre']['location']['latitude'], movie['attributes']['theatre']['location']['longitude']], location)})",
        })

    return recommendations

# Function to optimize the schedule and pick the optimal time for reservations
def optimize_schedule(dinner_time, movie_time, concert_time):
    # Add your optimization logic here (e.g., considering travel time, preferences, etc.)
    # This is a simple example where we pick the earliest time for each activity
    return dinner_time, movie_time, concert_time

# User inputs
cuisine = input("Enter preferred cuisine: ")
dietary_restriction = input("Enter any dietary restrictions: ")
date = input("Enter date (YYYY-MM-DD): ")
location = input("Enter location (latitude,longitude): ")
travel_distance = float(input("Enter how many miles willing to travel between each location: "))
movie_genre = input("Enter preferred movie genre: ")

# Convert date inputs to datetime objects
date = datetime.strptime(date, "%Y-%m-%d").date()

# Set initial times for each activity
dinner_time = datetime.combine(date, time(18, 0))  # 6:00 PM
movie_time = datetime.combine(date, time(20, 0))