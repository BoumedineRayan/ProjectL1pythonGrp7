
import os
import string
import math
from collections import defaultdict
import re


def extract(file):  # Definition of the extract function
    with open(file, "r",encoding='utf-8') as f:  # Opens the file in read mode
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

        with open(inputpath, "r", encoding='utf-8') as inputfile:
            contentofthefile = inputfile.read().lower()  # convert to lower case and store in a variable


        with open(outputpath, "w",encoding='utf-8') as outputfile:
            outputfile.write(contentofthefile)  # write the converted text into a new document
            # in the Cleaned directory
FCleaner()



def remove_punctuation(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r',encoding='utf-8') as f:
            text = f.read()

        # replace apostrophe with space
        text = text.replace("'", " ")

        # replace dash with space
        text = text.replace("-", " ")

        # remove newline characters
        text = text.replace("\n", " ")

        # remove punctuation characters
        text = text.translate(str.maketrans('', '', string.punctuation))

        with open(filepath, 'w',encoding='utf-8') as f:
            f.write(text)


remove_punctuation("Cleaned")


def calculate_tf(s):
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




def idf_count(directory):
    files = os.listdir(directory)  # List all the files in the directory
    num_docs = len(files)  # Count the total number of documents (files)

    doc_counts = defaultdict(int)  # Create a dictionary to store the number of documents containing each word
    idf_scores = defaultdict(float)  # Create a dictionary to store the IDF scores for each word

    for file in files:
        with open(os.path.join(directory, file), 'r',encoding='utf-8') as f:
            content = f.read()  # Read the content of the file
            words = content.split()  # Split the content into individual words

        unique_words = set(words)  # Use a set to count each word only once per document
        for word in unique_words:
            doc_counts[word] += 1  # Increment the count for the current word in the doc_counts dictionary

    for word, count in doc_counts.items():
        if count != 0:
            idf_scores[word] = round(math.log10((num_docs / count)) + 1 ,5)# Calculate the IDF score for the current word and store it in the idf_scores dictionary
        else:
            idf_scores[word] = float('inf')  # Handle the case where count is zero (word appears in all documents)

    return idf_scores  # Return the IDF scores for all the words in the directory



def tfidf(directory):
    files = os.listdir(directory)
    num_docs = len(files)

    doc_counts = defaultdict(int)
    idf_scores = defaultdict(float)

    # Step 1: Calculate document frequencies for each word.
    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            content = f.read()
            words = content.split()

        unique_words = set(words)
        for word in unique_words:
            doc_counts[word] += 1


    # Step 2 : Calculate the idf by using the previous IDF_count() function
    idf_scores = idf_count(directory)

    # Step 3: Calculate term frequencies (TF) for each word in each document.
    word_counts = {}
    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            content = f.read()
            words = content.split()

        unique_words = set(words)
        word_count = {}
        for word in unique_words:
            count = words.count(word)
            word_count[word] = count
        word_counts[file] = word_count

    # Step 4: Calculate the TF-IDF scores for each word in each document.
    tfidf_matrix = {}
    unique_words = set(word for file in files for word in word_counts[file].keys())
    for word in unique_words:
        tfidf_matrix[word] = []
        for file in files:
            tf = 0
            if word in word_counts[file]:
                tf = word_counts[file][word]
            idf = idf_scores[word]
            tfidf_matrix[word].append(tf * idf)

    return tfidf_matrix




def least_important_words(tfidf_matrix):
    # Implement code to display the list of least important words
    unimportant_words = [word for word, scores in tfidf_matrix.items() if all(score == 0 for score in scores)]
    return unimportant_words

def highest_tfidf_words_sum(directory):
    tfidf_matrix = tfidf(directory)
    # Calculate the sum of TF-IDF scores for each word across all documents
    word_sum_tfidf = {word: sum(tfidf_vector) for word, tfidf_vector in tfidf_matrix.items()}
    # Find the word(s) with the highest sum of TF-IDF scores
    highest_tfidf_words = max(word_sum_tfidf, key=word_sum_tfidf.get)
    return highest_tfidf_words

def repeat_word(directory, president_name):
    tf_president = {}
    for file in os.listdir(directory):
        if president_name not in str(file): continue
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            tf_dict = calculate_tf(file.read())
            for word, tf in tf_dict.items():
                if word not in tf_president:
                    tf_president[word] = 0
                tf_president[word] = tf_president[word] + tf

    most_repeated_word = max(tf_president, key=tf_president.get)
    return most_repeated_word


def presidents_speaking_nation(directory):
    freq_nation = {}
    max_freq = 0
    president_max = ""

    for file in os.listdir(directory):
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file_content:
            content = file_content.read()
            count = content.count("nation")
            if count > 0:
                president = re.match(r"Nomination_([a-zA-Z\s]+)(\d*)\.txt", file).group(1)
                freq_nation[president] = freq_nation.get(president, 0) + count
                if freq_nation[president] > max_freq:
                    max_freq = freq_nation[president]
                    president_max = president

    return president_max


def first_president_to_mention_topic(directory, topic):
    first_mention = None

    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as file_content:
            content = file_content.read()

            # Check if the topic is mentioned in the content
            if topic.lower() in content.lower():
                president = re.match(r"Nomination_([a-zA-Z\s]+)(\d*)\.txt", file).group(1)

                # Update the first_mention only if it's not set yet
                if first_mention is None:
                    first_mention = president

    return first_mention

def words_mentioned_by_all_presidents(tfidf_matrix, unimportant_words):
    # Implement code to identify words mentioned by all presidents (excluding unimportant words)
    all_presidents_words = set(tfidf_matrix.keys())
    for word in unimportant_words:
        all_presidents_words.discard(word)
    return list(all_presidents_words)



def menu():
    print("Hello and welcome in the project of Leo Carouge and Rayan Boumedine !" + '\n' +
                          "here we have different choices to go through our project :"+'\n'+
                          "Type 1 if you want to go to the basics functions :  " + '\n'+
                          "Type 2 if you want to go to the TF, IDF, TF-IDF Functions :  "+ '\n'+
                          "Type 3 if you want to leave the project ")
    answer = int(input("Your answer : "))
    if answer == 1:
        print("which function do you want to execute ?"+ '\n' +
              "Type 1 if you want to execute the extract(file) function :  " + '\n' +
              "Type 2 if you want to execute the FstName(name) function :  " + '\n' +
              "Type 3 if you want to execute the LofNames(dic) function :  " + '\n' +
              "Type 4 if you want to execute the remove_punctuation(directory) function :  " + '\n' +
              "Type 5 if you want to execute the FCleaner() function :  " + '\n' +
              "Type 6 if you want to leave the project :  ")
        choice=int(input())
        if choice==1:
            print(extract()) 
        elif choice==2:
            print()
        elif choice==3:
            print()
        elif choice==4:
            print() 
        elif choice==5:
            print() 
        elif choice==6:
            print()

    if answer == 2:
        print("which function do you want to execute ?" + '\n' +
              "Type 1 if you want to execute the calculate_tf(s)) function :  " + '\n' +
              "Type 2 if you want to execute the idf_count(directory) function :  " + '\n' +
              "Type 3 if you want to execute the LofNames(dic) function :  " + '\n' +
              "Type 4 if you want to leave the project :  ")
        choice=int(input())
