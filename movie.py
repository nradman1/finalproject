import requests
api_key = "0641c23b5695d5fe7a2586f40b784f59bbc6392ccf71d37e112778560f327e7e"
import requests

def get_events_data(city, date):
    """
    This function takes a city name and date, and grabs data from Google events on that day.
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
            link = event_result.get('link', 'N/A')

            event_info = [title, {
                'start_time': start_time,
                'address': address,
                'link': link
            }]

            events_data.append(event_info)

    return events_data

# Example usage:



def main():
    
    city = "Wellesley"
    date = "2023-12-03"
    events_data = get_events_data(city, date)
    print(events_data)

if __name__ == "__main__":
    main()
