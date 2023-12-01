import requests
import pprint
from bs4 import BeautifulSoup
from config import YELP_API_KEY

api_key = YELP_API_KEY  
base_url = 'https://api.yelp.com/v3/businesses/search'
headers = {"Authorization":f"Bearer {api_key}","accept":"application/json"}
api_endpoint = "https://api.yelp.com/v3/autocomplete?text=del&latitude=37.786882&longitude=122.399972"


def get_full_reviews(town, restaurant_name, limit=10):
    """
    Given the town and name of a restaurant, this code gets the full text of reviews for the specified restaurant.
    """
    full_reviews = []  # Initialize an empty list for all reviews

    response = requests.get(f"{base_url}?term={restaurant_name}&location={town}&limit=1", headers=headers)
    data = response.json()
    print(data)
    if 'businesses' in data and data['businesses']:
        business_id = data['businesses'][0]['id']
        reviews_endpoint = f"https://api.yelp.com/v3/businesses/{business_id}/reviews?limit={limit}&sort_by=relevance"
        reviews_response = requests.get(reviews_endpoint, headers=headers)

        reviews_data = reviews_response.json()

        if 'reviews' in reviews_data:
            for review in reviews_data['reviews']:
                review_url = review['url']
                full_review = scrape_review_text(review_url)
                full_reviews.append(full_review)

        else:
            print("No reviews found.")
    else:
        print(f"Restaurant '{restaurant_name}' not found in '{town}'.")

    for review in full_reviews:
        print(review)


def scrape_review_text(review_url):
    """
    Given a Yelp review URL, this function scrapes the full text of the review.
    """
    response = requests.get(review_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    review_text_element = soup.find('div', {'class': 'lemon--div__373c0__1mboc', 'lang': 'en'})
    
    if review_text_element:
        review_text = review_text_element.get_text(strip=True)
        return review_text
    else:
        return "Unable to retrieve review text."


def main():
    town = 'New York'  # Replace with the desired town
    restaurant_name = "Xi'an Famous Foods"
    get_full_reviews(town, restaurant_name)

if __name__ == "__main__":
    main()