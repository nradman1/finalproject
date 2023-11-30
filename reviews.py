import pprint
import requests
from bs4 import BeautifulSoup

api_key = "p_kmm2VPrX5yjTLQLlQ7DWXx1f2OIybVQNAJCFBg2OHLrbI-OokPZEBeaMIOBHZ15Gy9_RwsycIBYIusmcfOhaUJoYDkd6ZGymIKQAxUEyaDiLHGG3Sxq6aLaHJaZXYx"
headers = {"Authorization":f"Bearer {api_key}","accept":"application/json"}
api_endpoint = "https://api.yelp.com/v3/autocomplete?text=del&latitude=37.786882&longitude=122.399972"
    

def search_example():
    """
    This code pulls an example of the results as an exmplae so we hae a better understanding of what is within the code, it includes the businesses, cateogires, and terms 
    """
    response = requests.get(api_endpoint, headers=headers)
    pprint.pprint(response.json())

def get_reviews(businessname):
    """
    Given the "name-town" of a restaurant, this code gets the ID, rating, and the partial of the text for at least 3 all of the different interviews of the restaurant
    """
    
    api_endpoint = f"https://api.yelp.com/v3/businesses/{businessname}/reviews?limit=20&sort_by=yelp_sort"
    response = requests.get(api_endpoint, headers=headers)
    pprint.pprint(response.json())

def list_of_reviews(businessname):
    """
    This will make a list of each of the revies so we can analyze their sentimet 
    the reviews endpoint provides links to each review, then you can scrape the full text
    """
    pass

def time_of_review(businessname):
    

def main():
#    search_example()
   get_reviews("juniper-wellesley")
          
if __name__ == "__main__":
    main()