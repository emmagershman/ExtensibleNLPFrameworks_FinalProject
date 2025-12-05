# 1) SANKEY DIAGRAM (REQUIRED)
    # ---------------------------------------------------------------------
    def wordcount_sankey(
        self,
        word_list: Optional[List[str]] = None,
        k: int = 5,
        title: str = "Text-to-Word Sankey Diagram",
    ) -> None:
        """
        Text-to-Word Sankey diagram.
        - If word_list is provided: use those words
        - Else: use the union of the k most common words for each text
        """

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
