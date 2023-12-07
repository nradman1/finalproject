import requests

def get_movie_theaters_data(query, location):
    """
    This function retrieves showtimes information for a given movie or theater.
    """
    url = (
        f"https://serpapi.com/search.json?q={query}&location={location}&hl=en&gl=us&api_key=0641c23b5695d5fe7a2586f40b784f59bbc6392ccf71d37e112778560f327e7e"
    )

    response = requests.get(url)
    results = response.json()

    if "showtimes" in results:
        showtimes_data = results["showtimes"]
        return showtimes_data
    else:
        print("No showtimes data found.")
        return []

# Example usage:
query = "AMC Barton Creek Square 14"
location = "Austin, Texas, United States"


theater_data = get_movie_theaters_data(query, location)
print(theater_data)