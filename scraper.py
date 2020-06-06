#python -m venv_enviornment_folder_name venv
#venv\Scripts\activate  ---> not in powershell(activating the virtual environment)
#pip install beautifulsoup4


# importing required all the in-built library
import requests, json
from bs4 import BeautifulSoup

# all the urls which are used for scraping
URL_LISTS = ['https://khatrimaza1.kim/' ,'https://themoviesflix.in/', 'https://moviesflixpro.in/#.XLJGY-gzbIU', 'https://reqzone.com/movie/']


# function for getitng response and status_code of url  
def find_status_code(url):
    '''
    taking url and returning response and status_code
    '''
    try:
        res = requests.get(url)
        status_code = res.status_code
        return status_code, res
    except:
        pass


# Scraping data from khatrimaza website
def parser_data_khatrimaza(soup, MOVIES):
    '''
    Scraping data from khatrimaza website and storing title,image and download_link as dictionary and appending the MOVIES list 
    '''
    try:
        for content in soup.select("figure"):
            # print(content.select('img')[0]['src'])
            # print(content.select('img')[0]['title'])
            # print(content.select('a')[0]['href'])
            # print()
            title = content.select('img')[0]['title'].strip()
            image = content.select('img')[0]['src'].strip()
            download_link = content.select('a')[0]['href'].strip()
            MOVIES.append({'title': title, 'image': image, 'download': download_link})
    except:
        pass


# Scraping data from reqzone website
def parser_data_reqzone(soup, MOVIES):
    '''
    Scraping data from reqzone website and storing title,image and download_link as dictionary and appending the MOVIES list 
    '''
    try:
        for content in soup.select('.archive-container'):
                for movie_title,movie_poster in zip(content.select('.movie-title'),content.select('.movie-poster')):
                    # print(movie_poster.select('img')[0]['src'])
                    # print(movie_title.select('a')[0]['href'])
                    # print(movie_title.select('a')[0].text.strip())
                    # print()
                    title = movie_title.select('a')[0].text.strip()
                    image = movie_poster.select('img')[0]['src'].strip()
                    download_link = movie_title.select('a')[0]['href']
                    MOVIES.append({'title': title, 'image': image, 'download': download_link})
    except:
        pass


# Scraping data from moviesflix website
def parser_data_other(soup, MOVIES):
    '''
    Scraping data from moviesflix website and storing title,image and download_link as dictionary and appending the MOVIES list 
    '''
    try:
        for content in soup.select("article"):
            # print(content.select('img')[0]['src'])
            # print(content.select('a')[0]['title'])
            # print(content.select('a')[0]['href'])
            # print()
            image = content.select('img')[0]['src'].strip()
            title = content.select('a')[0]['title'].strip()
            download_link = content.select('a')[0]['href'].strip()
            MOVIES.append({'title': title, 'image': image, 'download': download_link})
    except:
        pass


# Scraping data from reqzone website for searched movie name
def parser_data_reqzone_search(soup, MOVIES):
    '''
    Scraping data from reqzone website and storing title,image and download_link as dictionary and appending the MOVIES list for searched movie name
    '''    
    try:
        for content in soup.select("article"):
            # print(content.select('a')[0]['href'])
            # print(content.select('img')[0]['src'])
            # print(content.select('img')[0]['alt'])
            # print()
            image = content.select('img')[0]['src'].strip()
            title = content.select('img')[0]['alt'].strip()
            download_link = content.select('a')[0]['href'].strip()
            MOVIES.append({'title': title, 'image': image, 'download': download_link})
    except:
        pass


# saving the retrieved data into the json file as a cached data
def cache_save(movies):
    '''
    taking movies list as input and storing into the json file
    '''
    filename = open('cache.json','w')
    json.dump(movies,filename)


# main function which operate for server module or testing purpose
def main(search_input = None):
    '''
    take input as movie name if you want to search else finding the leatest movies from all websites (its calling all the functions which already created into this module) 
    '''
    MOVIES = []
    if not search_input:
        try:
            for url in URL_LISTS:
                status_code,res = find_status_code(url)

                if status_code == 200:

                    soup = BeautifulSoup(res.text, 'html.parser')
            
                    if 'khatrimaza' in url:
                        parser_data_khatrimaza(soup, MOVIES)
                    
                    if 'reqzone' in url:
                        parser_data_reqzone(soup, MOVIES)

                    if 'khatrimaza' not in url and 'reqzone' not in url: 
                        parser_data_other(soup, MOVIES)

                    if len(MOVIES)>0:
                        cache_save(MOVIES)
        except:
            pass

    else:
        try:
            for url in URL_LISTS:
                if 'moviesflix' not in url:
                    url = url+'?s='+search_input
                    status_code,res = find_status_code(url)
                    if status_code == 200:
                        soup = BeautifulSoup(res.text, 'html.parser')
                
                        if 'khatrimaza' in url:
                            parser_data_khatrimaza(soup, MOVIES)
                        
                        if 'reqzone' in url:
                            parser_data_reqzone_search(soup, MOVIES)

        except:
            pass
    
    return MOVIES


# function which is used for the testing purpose 
def display():
    '''
    printing the movies data
    '''
    movies = main(search_input='The Big Short')
    from pprint import pprint
    pprint(movies)


if __name__ == '__main__':
    display()
    

