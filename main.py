
import os
import string
import math
from collections import defaultdict


def extract(file):  # Definition of the extract function
    with open(file, "r") as f:  # Opens the file in read mode
        d = {
            "Nomination_Chirac1.txt": "Chirac",
            "Nomination_Chirac2.txt": "Chirac",
            "Nomination_Giscard dEstaing.txt": "Giscard d'Estaing",
            "Nomination_Hollande.txt": "Hollande",
            "Nomination_Macron.txt": "Macron",
            "Nomination_Mitterrand1.txt": "Mitterrand",
            "Nomination_Mitterrand2.txt": "Mitterrand",
            "Nomination_Sarkozy.txt": "Sarkozy",
        }

        return d.get(f.name)  # Returns the value associated with the key corresponding to the file name

# Calling the extract function with the file "Nomination_Mitterrand2.txt"
# print(extract("Nomination_Mitterrand2.txt"))


def FstName(name):
    # Dictionary mapping last names to first names of presidents
    president_names = {
        "Chirac": "Jacques",
        "Giscard d'Estaing": "Valéry",
        "Hollande": "François",
        "Macron": "Emmanuel",
        "Mitterrand": "François",
        "Sarkozy": "Nicolas",
    }

    # Using the get method to retrieve the first name for the given last name
    # If the last name is not found, it will return None
    return president_names.get(name)

# Example usage: calling the function with the last name "Chirac"
result = FstName("Chirac")

# Displaying the result
#print(result)

president_names = {
    "Chirac": "Jacques",
    "Giscard d'Estaing": "Valéry",
    "Hollande": "François",
    "Macron": "Emmanuel",
    "Mitterrand": "François",
    "Sarkozy": "Nicolas",
}


def LofNames(dic):
    L = [] # creation of a List L
    for element, value in dic.items(): # Using dic.items() helps us to iterate on key/value pairs
        if element not in L: # Check if the name is already in the list
            L.append(element)  # adding the key of the dictionary to the List L
    return L


def FCleaner():
    filenames = [
        "Nomination_Chirac1.txt",
        "Nomination_Chirac2.txt",
        "Nomination_Giscard dEstaing.txt",
        "Nomination_Hollande.txt",
        "Nomination_Macron.txt",
        "Nomination_Mitterrand1.txt",
        "Nomination_Mitterrand2.txt",
        "Nomination_Sarkozy.txt",
    ]

    # Create the "cleaned" directory
    cleaned_dir = "Cleaned"  # Set the name of the directory as "Cleaned"
    if not os.path.exists(cleaned_dir):
        os.mkdir(cleaned_dir)  # Create the directory

    # Iterate on the dictionary
    for filename in filenames:
        inputpath = os.path.join("speeches", filename)  # Construct a path to the original file in the "speeches" directory
        outputpath = os.path.join(cleaned_dir, filename)  # constructs the o,
        # which is the path where the cleaned file will be saved

        with open(inputpath, "r") as inputfile:
            contentofthefile = inputfile.read().lower()  # convert to lower case and store in a variable


        with open(outputpath, "w") as outputfile:
            outputfile.write(contentofthefile)  # write the converted text into a new document
            # in the Cleaned directory
FCleaner()



def remove_punctuation(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            text = f.read()

        # replace apostrophe with space
        text = text.replace("'", " ")

        # replace dash with space
        text = text.replace("-", " ")

        # remove newline characters
        text = text.replace("\n", " ")

        # remove punctuation characters
        text = text.translate(str.maketrans('', '', string.punctuation))

        with open(filepath, 'w') as f:
            f.write(text)


remove_punctuation("Cleaned")


def Tf(s):
    # Split the string into words
    words = s.split()

    # Initialize an empty dictionary
    word_dict = {}

    # Iterate over each word in the list
    for word in words:
        # If the word is already in the dictionary, increment its count
        if word in word_dict:
            word_dict[word] += 1
        # Otherwise, add the word to the dictionary with a count of 1
        else:
            word_dict[word] = 1

    # Return the completed dictionary
    return word_dict




def idf_score(directory):
    files = os.listdir(directory)  # List all the files in the directory
    num_docs = len(files)  # Count the total number of documents (files)

    doc_counts = defaultdict(int)  # Create a dictionary to store the number of documents containing each word
    idf_scores = defaultdict(float)  # Create a dictionary to store the IDF scores for each word

    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            content = f.read()  # Read the content of the file
            words = content.split()  # Split the content into individual words

        unique_words = set(words)  # Use a set to count each word only once per document
        for word in unique_words:
            doc_counts[word] += 1  # Increment the count for the current word in the doc_counts dictionary

    for word, count in doc_counts.items():
        if count != 0:
            idf_scores[word] = math.log10(num_docs / count)  # Calculate the IDF score for the current word and store it in the idf_scores dictionary
        else:
            idf_scores[word] = float('inf')  # Handle the case where count is zero (word appears in all documents)

    return idf_scores  # Return the IDF scores for all the words in the directory




def tfidf(directory_path):
    # Get the list of file paths in the specified directory
    file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

    # Read the content of each file
    documents = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            documents.append(content)

    # Use Tf and idf_score functions to calculate TF-IDF matrix
    tfidf_values = []
    idf_scores = idf_score(directory_path)
    for document in documents:
        tf_values = Tf(document)
        tfidf_values.append({word: tf * idf_scores[word] for word, tf in tf_values.items()})

    # Convert the TF-IDF matrix to a list of dictionaries for better readability
    return tfidf_values

print(tfidf("Cleaned"))








