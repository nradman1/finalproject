# Overview

 A lot of times when trying to plan the perfect date, things get extremely overwhelming. Google searches provide a never-ending amount of information to scroll through which can confuse the planner. Plan the Perfect date simplifies things for the user, requiring only town name and date as inputs, and providing a simple list of a fun event as well as top ranked restaurants in the area in order to quickly plan the perfect date!

# How to Use

In order to run this code, we have created a flask page that will run everything once you open the site. In order to get the code to run, please go to app.py and click run, then hit the link and you will be able to see the site on Flask! Please see the video demo on the website [LINK] in order to get an idea of how the website works! It is as simple as entering your city and the date! See below for the list of user inputs, functions, and output in the flowchart! 

## Libraries

The libraries that must be installed for this code to work are json, urllib, requests, and beautiful soup, in order to get and parse the data, as well as flask to run the site. There are no input files required for this code. 

If you just want to run the code, and not the flask site, that is possible as well! There is some test code at the bottom of each page so you can see how all of the individual pieces of code work! 

## About the Code

### Events.py
On the events.py the functions include get_events_data, which pulls the name, date, address, time, and link of the events, the next function formats it, then after, event_interested_in, takes the name of the event you are interested in and returns the link! 

### Yelp.py

On yelp.py the function get_lat_long uses mapbox to get the latitude and longitude given a place name, this is then used within get nearest restaurants, to get a list of the nearest restaurants to your latitude and longitude. Afterwards, there is a function that ranks the restaurants, and another one that sorts it by the cuisine. Lastly, there is a piece of code that states if the restaurants are open within 2 hours of the time entered, however, many restaurants do not have time within it, so it did not work. 

### Reviews.py

The reviews.py pulls yelp reviews, which shows a bit of information from 3 reviews, allowing the user to have a snapshot of user input.

### Movies.py

The movies.py files goal was to find movies and movie times. We intended to implement it in the flask as another level for Plan a Perfect Date. Unfortunately, it became counterintuitive as the user would have needed to enter the movie theaters exact address. In the end we decided not to include it. 