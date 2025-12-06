"""
Names: Emma Gershman, Lydia Lutake, Chipego Nkolola, Suraj Swamy
Professor: John Rachlin
Course: Advanced Programming with Data
Extensible NLP Framework
"""

# URls for reference - sources of historical letters
URL = 'https://newsinteractives.cbc.ca/longform/remember-that-i-love-you-a-soldiers-letters-to-his-sweetheart/'
URL2 = 'https://blog.forceswarrecords.com/love-letter-from-a-world-war-one-soldier/'
URL3 = 'https://www.iwm.org.uk/history/letters-to-loved-ones'

from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import json
import string
from textblob import TextBlob
import plotly.graph_objects as go
import pandas as pd
import math
from wordcloud import WordCloud

# Filename for the stop words list (common words to filter out)
STOP_WORDS_FILENAME = 'stop_words.txt'

# Main class for analysisng and visualizing letter text data
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

    @staticmethod
    def default_parser(filename):
        """ For processing plain text files (.txt) """
        # Open and read the text file
        with open(filename, "r", encoding='utf-8') as f:
            text = f.read()
            # Convert to lowercase for consistency
            text = text.lower()
            # Remove all punctuation marks
            text = text.translate(str.maketrans('', '', string.punctuation))
            # Split text into individual words
        word_lst = text.split()
        # Filter out stop words to focus on meaningful words
        filtered_words = [word for word in word_lst if word not in Letters.load_stop_word(STOP_WORDS_FILENAME)]
        # Create results dictionary with word counts and metadata
        results = {
            'wordcount': Counter(filtered_words),
            'numwords': len(filtered_words),
            'fulltext': filtered_words
        }

        print("Parsed ", filename, ": ", results)
        return results

    @staticmethod
    def json_parser(filename):
        # Open and load JSON file
        f = open(filename)
        raw = json.load(f)
        # Extract text from JSON
        text = raw['text']
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Split into words
        words = text.split(" ")
        # Count word frequencies
        wc = Counter(words)
        # Count total words
        num = len(words)
        f.close()
        return {'wordcount': wc, 'numwords': num}

    def load_text(self, filename, label=None, parser=None):
        """ Register a text document with the framework.
         Extract and store data to be used later in our visualizations.
         Done by Emma Gershman"""
        # Use default parser if none is specified
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

        # iterate through results and organize by data type
        for k, v in results.items():
            self.data[k][label] = v


    def compare_num_words(self):
        """ A very simplistic visualization that creates
        a bar chart comparing num words for each text file
        For HW7, I expect much more interesting visualizations """
        # Create figure with specified size
        plt.figure(figsize=(10, 6))
        # Get word count data for all loaded texts
        numwords = self.data['numwords']
        # Create a bar for each text file
        for label, nw in numwords.items():
            plt.bar(label, nw)
        # Add ads labels and title
        plt.xlabel('Text File')
        plt.ylabel('Number of Words')
        plt.title('Wordcount for Letters')
        # Rotate x-axis labels for readability
        plt.xticks(rotation=45)
        # Adjust layout to prevent label cutoffs
        plt.tight_layout()
        plt.show()


        
    def wordcount_sankey(self, word_list=None, k=5):
        """
        Create a Sankey diagram mapping each loaded text (label) to words.
        Function done by Suraj Swamy
        """

        # Make sure we have wordcount data
        if "wordcount" not in self.data or not self.data["wordcount"]:
            print("No wordcount data available. Make sure to call load_text() first.")
            return

        # Get a list of all text lables
        text_labels = list(self.data["wordcount"].keys())
        wordcounts = self.data["wordcount"]

        # If there's no word list supplied, build one from top-k of each text
        if word_list is None:
            word_set = set()
            # Collect most common k words from each text
            for label in text_labels:
                wc = wordcounts[label]
                for word, _ in wc.most_common(k):
                    word_set.add(word)
            # Sort words alphabetically
            word_list = sorted(word_set)

        # Create node labels: texts first, then words
        text_nodes = text_labels
        word_nodes = word_list
        node_labels = text_nodes + word_nodes

        # Map each label to an index in node_labels
        node_index = {name: i for i, name in enumerate(node_labels)}

        # List to store link data
        sources = []
        targets = []
        values = []

        # Create links from each text to each word 
        for text_label in text_nodes:
            wc = wordcounts[text_label]
            for word in word_nodes:
                # Get count of this word in text
                count = wc.get(word, 0)
                # Only create link if word appears in text
                if count > 0:
                    sources.append(node_index[text_label])
                    targets.append(node_index[word])
                    values.append(count)

        # Check if there's any data to visualize
        if not values:
            print("No data to show in Sankey diagram.")
            return

        # Create Sankey diagram using Plotly
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
           - Function done by Chipego Nkolola
        """

        # Get list of all loaded text labels
        labels = list(self.data['numwords'].keys())
        num_files = len(labels)

        # Determine grid size (square-ish)
        cols = math.ceil(math.sqrt(num_files))
        rows = math.ceil(num_files / cols)

        # Create subplot grid
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), sharey = True)

        # Handle single subplot case
        if num_files == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        # Create bar chart for each text file
        for i, label in enumerate(labels):
            # Get total and unique word counts
            total_words = self.data['numwords'][label]
            unique_words = len(self.data['wordcount'][label])

            # Set up bar positions and values
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

        # Add overall title and adjust alyout
        plt.suptitle('Word Count Comparison: Total v. Unique')
        plt.tight_layout()
        plt.show()

    def word_cloud(self, cols=4, **misc_parameters):
        """Creates a word cloud based off the word count
        Done by Emma Gershman"""

        # Get list of all text labels
        labels = list(self.data["wordcount"].keys())
        n = len(labels)

        # Check if there's no data to visualize
        if n == 0:
            print("No data to visualize")
            return

        # Calculate number or rows needed
        rows = math.ceil(n / cols)
        # Create subplot grid
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))

        # Handle single subplot case
        if n == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        # Create word cloud for each text
        for i, label in enumerate(labels):
            word_freq = self.data["wordcount"][label]

            # Generate word cloud from word frequencies
            wc = WordCloud(
                width=400,
                height=400,
                background_color='white'
            ).generate_from_frequencies(word_freq)

            # Display word cloud in subplot
            axes[i].imshow(wc, interpolation='bilinear')
            axes[i].axis('off')
            axes[i].set_title(label, fontsize=12)

        for j in range(n, len(axes)):
            axes[j].axis('off')


        # Add overall title and adjust layout
        plt.suptitle('Most Common Words in Letters to Loved Ones', fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()

    def Sentiment_curve(self, **misc_parameters):
        """
        Create a single visualization that overlays data from each text file
        compare the polarities(positivity or negativity) of different text files from beigning to end
        Done by Lydia Lutake"""

        # Create a Plotly figure
        fig = go.Figure()
        # Get list of all text labels
        labels = list(self.data["fulltext"].keys())

        # Process each text file
        for label in labels:
            # Compute sentiment for each word
            words = self.data["fulltext"][label]
            # Calculate polarity (-1 to 1) for each word
            polarities = [TextBlob(word).sentiment.polarity for word in words]
            # Apply rolling average to smooth the curve 
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

