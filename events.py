import requests

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
            link = event_result.get('link', 'N/A')

            event_info = [title, {
                'start_time': start_time,
                'address': address,
                'link': link
            }]

            events_data.append(event_info)

        return events_data

def formatted_data(city, date):
    """
    This function formats the data form the def get_events_data function into a list of functions more easy to read
    """
    events_list = get_events_data(city, date)
    for event in events_list:
        title = event[0]
        event_details = event[1]
        start_time = event_details['start_time']
        address = ', '.join(event_details['address'])

        print(f"Event Name: {title} - Start Time: {start_time} - Address: {address}\n")    

def event_interested_in(city, date, event_name):
    """
    This takes the name of the event you are interested in, and returns the link for the user to register for it on/see more details
    """
    events_list = get_events_data(city, date)
    for event in events_list:
        title = event[0]
        event_details = event[1]

        if title == event_name:
            link =  event_details.get('link')
            print(f"Registration Link for '{event_name}': {link}")


def main():
    
    city = "Wellesley"
    date = "2023-12-03"

    print(get_events_data(city, date))
    formatted_data(city, date)
    event_interested_in(city, date, "Wellesley Festival of Trees")

if __name__ == "__main__":
    main()
