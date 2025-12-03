URL = 'https://newsinteractives.cbc.ca/longform/remember-that-i-love-you-a-soldiers-letters-to-his-sweetheart/'
URL2 = 'https://blog.forceswarrecords.com/love-letter-from-a-world-war-one-soldier/'
URL3 = 'https://www.iwm.org.uk/history/letters-to-loved-ones'

import requests
from bs4 import BeautifulSoup

def retrieve_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return response