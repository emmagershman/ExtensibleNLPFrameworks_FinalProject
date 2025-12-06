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
import plotly.graph_objects as go
import pandas as pd
import random
import math
from wordcloud import WordCloud

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


        
    def wordcount_sankey(self, word_list=None, k=5):
        """
        Create a Sankey diagram mapping each loaded text (label) to words.
        """

        # Make sure we have wordcount data
        if "wordcount" not in self.data or not self.data["wordcount"]:
            print("No wordcount data available. Make sure to call load_text() first.")
            return

        
        text_labels = list(self.data["wordcount"].keys())
        wordcounts = self.data["wordcount"]

        # If there's no word list supplied, build one from top-k of each text
        if word_list is None:
            word_set = set()
            for label in text_labels:
                wc = wordcounts[label]
                for word, _ in wc.most_common(k):
                    word_set.add(word)
            word_list = sorted(word_set)

        
        text_nodes = text_labels
        word_nodes = word_list
        node_labels = text_nodes + word_nodes

        # Map each label to an index in node_labels
        node_index = {name: i for i, name in enumerate(node_labels)}

        sources = []
        targets = []
        values = []

        # Create links from each text to each word 
        for text_label in text_nodes:
            wc = wordcounts[text_label]
            for word in word_nodes:
                count = wc.get(word, 0)
                if count > 0:
                    sources.append(node_index[text_label])
                    targets.append(node_index[word])
                    values.append(count)

        if not values:
            print("No data to show in Sankey diagram.")
            return

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

        fig.update_layout(
            title_text="Text-to-Word Sankey Diagram",   # fixed title
            font_size=10,
            template="plotly_white"
        )

        fig.show(renderer="browser")





    def compare_words(self, **misc_parameters): #change name later
        """
        Creates a visualization array (subplot grid) with one subplot per text file.
        misc_parameters should contain a list of dictionaries with:
           - 'filename': name of file
           - 'text':     the text content of the file
        """

        labels = list(self.data['numwords'].keys())
        num_files = len(labels)

        # Determine grid size (square-ish)
        cols = math.ceil(math.sqrt(num_files))
        rows = math.ceil(num_files / cols)

        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), sharey = True)

        if num_files == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        for i, label in enumerate(labels):
            total_words = self.data['numwords'][label]
            unique_words = len(self.data['wordcount'][label])

            x_pos = [0,1]
            values = [total_words, unique_words]
            colors = ['#3498db', '#e74c3c']

            # Plot bar for each file
            axes[i].bar(x_pos, values, width = 0.5, color = colors)
            axes[i].set_xticks(x_pos)
            axes[i].set_xticklabels(['Total Words', 'Unique Words'])
            axes[i].set_title(label)
            axes[i].set_ylabel("Count")

        # Hide unused subplots if any
        for j in range(num_files, len(axes)):
            axes[j].axis('off')

        plt.suptitle('Word Count Comparison: Total v. Unique')
        plt.tight_layout()
        plt.show()

    def word_cloud(self, cols=4, **misc_parameters):
        labels = list(self.data["wordcount"].keys())
        n = len(labels)

        if n == 0:
            print("No data to visualize")
            return

        rows = math.ceil(n / cols)
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))

        if n == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        for i, label in enumerate(labels):
            word_freq = self.data["wordcount"][label]

            # Use a Windows system font
            wc = WordCloud(
                width=400,
                height=400,
                background_color='white'
            ).generate_from_frequencies(word_freq)

            axes[i].imshow(wc, interpolation='bilinear')
            axes[i].axis('off')
            axes[i].set_title(label, fontsize=12)

        for j in range(n, len(axes)):
            axes[j].axis('off')

<<<<<<< HEAD
        plt.suptitle('Most Common Words in Letters to Loved Ones', fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
=======
        plt.tight_layout()
        #plt.title('Word Cloud For Each Letter')
>>>>>>> 64a55f80011d12dc16586ad9b0d8615bcfa812ff
        plt.show()

    def Sentiment_curve(self, **misc_parameters):
        """
        Create a single visualization that overlays data from each text file
        compare the polarities(positivity or negativity) of different text files from beigning to end
        """
        fig = go.Figure()
        labels = list(self.data["fulltext"].keys())

        for label in labels:
            # Compute sentiment for each word
            words = self.data["fulltext"][label]
            polarities = [TextBlob(word).sentiment.polarity for word in words]
            polarities = pd.Series(polarities).rolling(window=5, min_periods=1).mean().tolist()

            # Percent position through the text
            place = [(i / len(words)) * 100 for i in range(len(words))]

            # Add line to Plotly figure
            fig.add_trace(go.Scatter(
                x=place,
                y=polarities,
                mode='lines',
                name=label,
            ))

        # graph label
        fig.update_layout(
            title="Sentiment Curve Comparison",
            xaxis_title="Progress Through Text (%)",
            yaxis_title="Sentiment Polarity",
            yaxis=dict(range=[-1, 1]),
            template="plotly_white"
        )

        fig.show(renderer="browser")

