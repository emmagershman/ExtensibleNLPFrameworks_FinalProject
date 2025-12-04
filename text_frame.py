
from collections import defaultdict, Counter


class TEXT:
    def __init__(self):
        self.stop_word = set() # A set of common or stop words
        self.data = defaultdict(dict)
        self.text = [] # list of dict of text

    def load_stop_word(self, stopfile):

        """ Load stop words into a set"""
        pass

    def load_text(self, filename, label=None, parser=None):
        """ Load text from a file"""
        pass

    def wordcount_sankey(self, word_list=None, k=5):
        """ Return number of words in text"""
        pass

    def second_visualization(self, **misc_parameters): #change name later
        """
        Create a multi-subplot visualization (one subplot per text).
        """
        pass


    def third_visualization(self, **misc_parameters):#change name later
        """
        Create a single visualization that overlays data from each text file.
        """
        pass
