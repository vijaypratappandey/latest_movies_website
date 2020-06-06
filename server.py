# importing required all the in-built library
from flask import Flask, render_template, request
import json

# importing created modules which have leatest movies
import scraper

# Returning all the leatest Movies 
MOVIES = scraper.main()

# Creating a function which retrieve the cached data
def cache_retrive():
    '''
    retrieve the cached data (previous scraped data)
    '''
    filename = open('cache.json','r')
    MOVIES = filename.readline()
    MOVIES = json.loads(MOVIES)

    return MOVIES

# if leatest data is not scraped the retrieve the cached data
if len(MOVIES)==0:
    MOVIES = cache_retrive()

# creates the Flask instance with same module name
app = Flask(__name__)

# Home page 
@app.route('/')
def home():
    '''
    Retreiving the leatest movies and display on the home page
    '''
    return render_template('index.html',movies=MOVIES)

# Search page
@app.route('/search', methods=['POST', 'GET'])
def search():
    '''
    taking input through the search bar and display the movies on search page if not available that movie then display Not Found(404)
    '''
    if request.method == 'POST':
        # taking data from form and converted into dictionary
        data = request.form.to_dict()
        # searching the movie name from the whole websites and returning as MOVIES list
        search_input = scraper.main(data.get('search_input'))
        # dealing with the NOT FOUND scenario
        if len(search_input)==0:
            search_input = [{'title':'Not Found','download':'./','image':'./static/not-found.png'}]

    return render_template('search.html', movies=search_input)
