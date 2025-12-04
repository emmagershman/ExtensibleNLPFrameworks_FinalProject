URL = 'https://newsinteractives.cbc.ca/longform/remember-that-i-love-you-a-soldiers-letters-to-his-sweetheart/'
URL2 = 'https://blog.forceswarrecords.com/love-letter-from-a-world-war-one-soldier/'
URL3 = 'https://www.iwm.org.uk/history/letters-to-loved-ones'

"""
# Create a framework class with, at minimum, the following methods:

# load_stop_words(stopfile) - not as time-consuming (Lydia)
# A list of common or stop words. These get filtered from each file automatically

# load_text(self, filename, label=None, parser=None) - time-consuming, have to make sure its universal for any file (Emma)
# Register a text file with the library. The label is an optional label you’ll use in your
# visualizations to identify the text

# wordcount_sankey(self, word_list=None, k=5) - time-consuming (Suraj)
# Map each text to words using a Sankey diagram, where the thickness of the line
# is the number of times that word occurs in the text. Users can specify a particular
# set of words, or the words can be the union of the k most common words across
# each text file (excluding stop words).

# your_second_visualization(self, misc_parameters) - Use plotly/matplotlib for this, not too difficult (Chipego)
# A visualization array of subplots with one subplot for each text file.
# Rendering subplots is a good, advanced skill to know!

# your_third_visualization(self, misc_parameters) - Use plotly/matplotlib, also not too difficult (Lydia)
# A single visualization that overlays data from each of the text files. Make sure your
# visualization distinguishes the data from each text file using labels or a legend

# self.data dictionary attribute and class TextFramework (Emma)
"""

import requests
from bs4 import BeautifulSoup

def retrieve_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return response