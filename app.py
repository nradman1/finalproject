from flask import Flask, render_template, request, redirect
from events import formatted_data, event_interested_in
from yelp import sorted_by_cuisine, get_nearest_restaurants, ranked, get_lat_long
from config import YELP_API_KEY
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/events', methods=['POST'])
def events():
    city = request.form['city']
    date = request.form['date']
    print(f"Received data: City - {city}, Date - {date}")

    events_data = formatted_data(city, date)
    print(events_data)
    if not city or not date: #exceptions
        return redirect('/error_page')

    return render_template('events.html', city=city, events_data=events_data)


@app.route('/restaurant_search', methods=['POST'])
def restaurant_search():
    if request.method == 'POST':
        city = request.form['city']
        price_range = request.form['price_range']  # Assuming the input will be a dropdown or similar with options like '$', '$$', '$$$', '$$$$'

        # Get latitude and longitude for the town
        latitude, longitude = get_lat_long(city)

        # Get nearest restaurants based on the selected price range
        restaurants = get_nearest_restaurants(YELP_API_KEY, latitude, longitude, radius_miles=5)

        # Filter restaurants based on the selected price range
        restaurants = [restaurant for restaurant in restaurants if restaurant.get('price') == price_range]

        return render_template('restaurant_search.html', city=city, price_range=price_range, restaurants=restaurants)

@app.route('/error_page')
def error_page():
    return render_template('error_page.html')


if __name__ == '__main__':
    app.run(debug=True)
