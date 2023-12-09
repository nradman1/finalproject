from flask import Flask, render_template, request, redirect
from events import formatted_data
from yelp import get_nearest_restaurants
import requests

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        # Handle the form submission
        city = request.form['city']
        date = request.form['date']
        print(f"Received data: City - {city}, Date - {date}")

        events_data = formatted_data(city, date)
        print(events_data)
        if not city or not date:
            return redirect('/error_page')

        return render_template('events.html', city=city, events_data=events_data)

    return render_template('index.html')

@app.route('/restaurant_search', methods=['POST'])
def restaurant_search():
    city = request.form.get('city')
    
    if city:
        restaurants = get_nearest_restaurants(city)
        if restaurants:
            return render_template('restaurant_search.html', city=city, restaurants=restaurants)
    
    return render_template('restaurant_search.html', city=city)

@app.route('/event_details/<int:event_id>', methods=['GET', 'POST'])
def event_details(event_id):
    event = {'title': 'Sample Event', 'start_time': '2023-12-06 18:00:00', 'address': 'Sample Address', 'id': event_id}

    if request.method == 'GET':
        return render_template('event_details.html', event=event)

@app.route('/event_details', methods=['POST'])
def event_details_post():
    return "Handle POST requests for event_details without event_id"
@app.route('/error_page')
def error_page():
    return render_template('error_page.html')

def get_events_data(city, date):
    """
    This event takes a city name and date, and grabs data from google events on that day
    """
    url = f"https://serpapi.com/search.json?engine=google_events&q=Events+in+{city}&hl=en&gl=us&date:{date}&api_key=0641c23b5695d5fe7a2586f40b784f59bbc6392ccf71d37e112778560f327e7e"
    response = requests.get(url)
    data = response.json()

    events_data = []
    if 'events_results' in data:
        for event_result in data['events_results']:
            title = event_result.get('title', 'N/A')
            start_time = event_result.get('date', {}).get('when', 'N/A')
            address = event_result.get('address', [])
            # Ensure the 'link' attribute is present and not empty
            link = event_result.get('link', '')

            event_info = [title, {
                'start_time': start_time,
                'address': address,
                'link': link
            }]

            events_data.append(event_info)

        return events_data

if __name__ == '__main__':
    app.run(debug=True)
