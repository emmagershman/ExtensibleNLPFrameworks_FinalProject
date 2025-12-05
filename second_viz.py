import matplotlib as plt
import math

def your_second_visualization(self, misc_parameters):
    """
    Creates a visualization array (subplot grid) with one subplot per text file.
    misc_parameters should contain a list of dictionaries with:
       - 'filename': name of file
       - 'text':     the text content of the file
    """

    files = misc_parameters.get("files", [])
    num_files = len(files)

    if num_files == 0:
        print("No files provided to visualize.")
        return

    # Determine grid size (square-ish)
    cols = math.ceil(math.sqrt(num_files))
    rows = math.ceil(num_files / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = axes.flatten()  # Flatten for easier indexing

    for i, file_data in enumerate(files):
        filename = file_data["filename"]
        text = file_data["text"]

        # Example metric → word count per file
        words = text.split()
        word_count = len(words)

        # Plot bar for each file
        axes[i].bar(["Word Count"], [word_count])
        axes[i].set_title(filename)
        axes[i].set_ylabel("Count")

    # Hide unused subplots if any
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

