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
import matplotlib.pyplot as plt
import json
import string
from textblob import TextBlob
from matplotlib.ticker import PercentFormatter

STOP_WORDS_FILENAME = 'stop_words.txt'

class Letters:

    def __init__(self):
        """ Constructor to initialize state """

        # Where all the data extracted from the loaded documents is stored
        self.data = defaultdict(dict)

    @staticmethod
    def load_stop_word(stopfile):

        """ Load stop words into a set"""
        with open(stopfile, 'r') as file:
            words = set([line.strip() for line in file])
        return words
    # def load(self, stopfile):
    #     with open(stopfile, 'r') as f:
    #         for line in f:
    #             word = line.strip()
    #             if word:
    #                 self.stop_word.append(word)

    @staticmethod
    def default_parser(filename):
        """ For processing plain text files (.txt) """
        with open(filename, "r", encoding='utf-8') as f:
            text = f.read()
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
        word_lst = text.split()
        filtered_words = [word for word in word_lst if word not in Letters.load_stop_word(STOP_WORDS_FILENAME)]
        results = {
            'wordcount': Counter(filtered_words),
            'numwords': len(filtered_words),
            'fulltext': filtered_words
        }

        print("Parsed ", filename, ": ", results)
        return results

    @staticmethod
    def json_parser(filename):
        f = open(filename)
        raw = json.load(f)
        text = raw['text']
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split(" ")
        wc = Counter(words)
        num = len(words)
        f.close()
        return {'wordcount': wc, 'numwords': num}

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
        plt.figure(figsize=(10, 6))
        numwords = self.data['numwords']
        for label, nw in numwords.items():
            plt.bar(label, nw)
        plt.xlabel('Text File')
        plt.ylabel('Number of Words')
        plt.title('Wordcount for Letters')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def second_visualization(self, **misc_parameters): #change name later
        """
        Create a multi-subplot visualization (one subplot per text).
        """
        pass


    def third_visualization(self, **misc_parameters):#change name later
        """
        Create a single visualization that overlays data from each text file.
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        labels = list(self.data["fulltext"].keys())
        for label in labels:
            polarities = [TextBlob(word).sentiment.polarity for word in self.data['fulltext'][label]]
            place = [(i/len(self.data['fulltext'][label])) * 100 for i in range(len(self.data['fulltext'][label]))]
            ax.plot(place, polarities, label=label)
        ax.set_xticks(range(0, 101, 10))
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=100))
        ax.set_xlim(0, 100)
        ax.legend()
        plt.tight_layout()
        plt.xlabel("Progress Through Letter (%)")
        plt.ylabel('Sentiment Polarity')
        plt.title('How Sentiment Changes Throughout the Letter')
        plt.show()

"""
    def wordcount_sankey(
        self,
        word_list: Optional[List[str]] = None,
        k: int = 5,
        title: str = "Text-to-Word Sankey Diagram",
    ) -> None:
        
        # Text-to-Word Sankey diagram.
        # - If word_list is provided: use those words
        # - Else: use the union of the k most common words for each text
        

        if "word_counts" not in self.data or not self.data["word_counts"]:
            raise ValueError("No texts loaded. Please call load_text first.")

        labels = list(self.data["word_counts"].keys())
        word_counts = self.data["word_counts"]

        # If user didn't supply a word list, build one from top-k of each text
        if word_list is None:
            word_set = set()
            for label in labels:
                counts = word_counts[label]
                for word, _ in counts.most_common(k):
                    word_set.add(word)
            word_list = sorted(word_set)

        # Build node list: first all text labels, then all words
        text_nodes = labels
        word_nodes = word_list

        node_labels = text_nodes + word_nodes

        # Map name -> index in node list
        node_index = {name: i for i, name in enumerate(node_labels)}

        sources = []
        targets = []
        values = []

        # For each text and each word, add a link if count > 0
        for text_label in text_nodes:
            counts = word_counts[text_label]
            for word in word_nodes:
                c = counts.get(word, 0)
                if c > 0:
                    sources.append(node_index[text_label])
                    targets.append(node_index[word])
                    values.append(c)

        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(width=0.5),
                        label=node_labels,
                    ),
                    link=dict(
                        source=sources,
                        target=targets,
                        value=values,
                    ),
                )
            ]
        )
        fig.update_layout(title_text=title, font_size=10)
        fig.show()
"""

