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
from collections import Counter, defaultdict
import random as rnd
import matplotlib.pyplot as plt

class Letters:

    def __init__(self):
        """ Constructor to initialize state """

        # Where all the data extracted from the loaded documents is stored
        self.data = defaultdict(dict)

    @staticmethod
    def default_parser(filename):
        """ For processing plain text files (.txt) """
        results = {
            'wordcount': Counter("to be or not to be".split(" ")),
            'numwords': rnd.randrange(10, 50)
        }

        print("Parsed ", filename, ": ", results)
        return results

    def load_text(self, filename, label=None, parser=None):
        """ Register a text document with the framework.
         Extract and store data to be used later in our visualizations. """
        if parser is None:
            results = Letters.default_parser(filename)
        else:
            results = parser(filename)

        # Use filename for the label if none is provided
        if label is None:
            label = filename

        # Store the results for that ONE document into self.data
        # For example, document A:  numwords=10,  document B: numwords=20
        # For A, the results are: {numwords:10}, for B: {numwords:20}
        # This gets stored as: {numwords: {A:10, B:20}}

        for k, v in results.items():
            self.data[k][label] = v


    def compare_num_words(self):
        """ A very simplistic visualization that creates
        a bar chart comparing num words for each text file
        For HW7, I expect much more interesting visualizations """

        numwords = self.data['numwords']
        for label, nw in numwords.items():
            plt.bar(label, nw)
        plt.show()