from config import YELP_API_KEY
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

api_key = YELP_API_KEY
MAPBOX_TOKEN = 'pk.eyJ1IjoibnJhZG1hbjEiLCJhIjoiY2xvcWR3NTRvMGZrbDJsbXpiOTltbXljbCJ9.K-LMaJZ0YTq4hvWv-wklbA'
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
headers = {"Authorization":f"Bearer {api_key}","accept":"application/json"}
api_endpoint = "https://api.yelp.com/v3/autocomplete?text=del&latitude=37.786882&longitude=122.399972"

import requests

def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_long() and get_nearest_station() might need to use this function.
    """
    #1. Uses urllib.request in order to open the url, setting it equal to f
    #2. read the content and decode it as a string using UTF-8, set it equal to the response text
    #3. set the data euqal to the text converted into a dictionary of the response text
    #4. return the response data
    with urllib.request.urlopen(url) as f:
        responsetxt = f.read().decode('utf-8')
        data = json.loads(responsetxt)
        return data

def get_lat_long(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    """
    #1. Replace the spaces in the place name, typical in URL coding
    #2. construct a URL to make the API request to Mapbox. Takes the URL name and the place name, and utilizes the access token for the API request in order to return the data in json format
    #3. set data euqal to the get_json function on the URL
    #4. print, within the data, get to the features line, get to the first element, go to the geometry dictionary, go to the coordinates list, select the second element, which is the latitude
    #5. same as above, except access the first element, which is the longitude at the end 
    MAPBOX_TOKEN = 'pk.eyJ1IjoibnJhZG1hbjEiLCJhIjoiY2xvcWR3NTRvMGZrbDJsbXpiOTltbXljbCJ9.K-LMaJZ0YTq4hvWv-wklbA'
    MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    query = place_name.replace(' ', '%20')
    url = f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}"
    data = get_json(url)

    latitude = str(round(float(data["features"][0]["geometry"]["coordinates"][1]),2))
    longitude = str(round(float(data["features"][0]["geometry"]["coordinates"][0]),2))

    return latitude, longitude 


def get_nearest_restaurants(latitude, longitude, radius_miles, sort_by='rating'):
    """
    Get a list of restaurants from Yelp within the specified latitude, longitude, and radius.

    """
    api_key = YELP_API_KEY
    base_url = 'https://api.yelp.com/v3/businesses/search'
    url = f'{base_url}?term=restaurants&latitude={latitude}&longitude={longitude}&radius={int(radius_miles * 1609.34)}&sort_by={sort_by}'
    headers = {'Authorization': f'Bearer {api_key}'}

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'businesses' in data:
        return data['businesses']
    else:
        print(f"Error retrieving data from Yelp API. Response: {data}")
        return []

def ranked(restaurants):
    """
    Rank restaurants by review rating and display the price.

    """
    if not restaurants:
        print("No restaurants provided.")
        return

    # Sort restaurants by review rating (descending order)
    ranked_restaurants = sorted(restaurants, key=lambda x: x['rating'], reverse=True)

    print("\nRanked Restaurants (by review rating):")
    for restaurant in ranked_restaurants:
        price = restaurant.get('price', 'N/A')
        print(f"{restaurant['name']} - Rating: {restaurant['rating']}, Price: {price}")

def sorted_by_cuisine(restaurants):
    """
    Sort restaurants by cuisine type and display the details.
    """
    if not restaurants:
        print("No restaurants provided.")
        return

    sorted_restaurants = sorted(restaurants, key=lambda x: x.get('categories', [{'title': 'Other'}])[0]['title'])

    print("\nSorted Restaurants (by cuisine):")
    for restaurant in sorted_restaurants:
        rating = restaurant.get('rating', 'N/A')
        price = restaurant.get('price', 'N/A')
        cuisine = restaurant.get('categories', [{'title': 'Other'}])[0]['title']
        print(f"{restaurant['name']} - Rating: {rating}, Price: {price}, Cuisine: {cuisine}")

#May just cut this whole entire thing as it does not really work well
def restaurants_open(town, radius_miles, day, time, sort_by='rating'):
    """
    Get a list of restaurants that are open within a ±2 hour window from the specified day and time from Yelp.

    """
    api_key = YELP_API_KEY
    latitude, longitude = get_lat_long(town)
    
    nearest_restaurants = get_nearest_restaurants(latitude, longitude, radius_miles, sort_by)

    # Convert input time to datetime object
    input_time = datetime.strptime(time, '%H:%M')

    # Define time window (+-2 hours)
    start_time = (input_time - timedelta(hours=2)).time()
    end_time = (input_time + timedelta(hours=2)).time()

    # Simplified list comprehension to filter out closed restaurants within the specified time window
    open_restaurants = [restaurant for restaurant in nearest_restaurants if not any(
        day['day'] == day and (day['start'] > end_time.strftime('%H:%M') or day['end'] < start_time.strftime('%H:%M')) for day in restaurant.get('hours', [])
    )]

    if not open_restaurants:
        print("No open restaurants found.")
        return

    print("\nThe Restaurants that are open within 2 hours of your ideal time:")
    for restaurant in open_restaurants:
        rating = restaurant.get('rating', 'N/A')
        price = restaurant.get('price', 'N/A')
        cuisine = restaurant.get('cuisine', 'N/A')
        name = restaurant['name']
        print(f"{name} - Rating: {rating}, Price: {price}, Cuisine: {cuisine}")


def main():
    # Example usage:
    place_name = 'Wellesley, MA'  # Replace with the desired place
    latitude, longitude = get_lat_long(place_name)

    # Removed the check for latitude and longitude
    radius_miles = 1  # Replace with the desired radius
    restaurants = get_nearest_restaurants(latitude, longitude, radius_miles)

    if restaurants:
        print("\nNearest Restaurants (sorted by rating):")
        for restaurant in restaurants:
            print(f"{restaurant['name']} - Rating: {restaurant['rating']}")

        ranked(restaurants)
        sorted_by_cuisine(restaurants)
    else:
        print("No restaurants found within the specified radius.")

    town = 'Wellesley, MA'
    radius_miles = 5
    day = 'Tuesday'
    time = '18:30'

    open_restaurants = restaurants_open(town, radius_miles, day, time, sort_by='rating')

    open_restaurants

if __name__ == "__main__":
    main()
