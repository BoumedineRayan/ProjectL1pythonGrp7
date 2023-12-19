
import os
import string
import math
from collections import defaultdict
import re


################### Part 1 : Basic functions #####################
def Extract_the_names_of_the_presidents(file):  # Definition of the extract function
    filepath = os.path.join("speeches", file)
    with open(filepath, "r") as f:  # Opens the file in read mode

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

        return d.get(file)  # Returns the value associated with the key corresponding to the file name

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

################### Part 2 : TF, IDF, TF-IDF #####################
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
            idf_scores[word] = round(math.log10((num_docs / count)) ,5)# Calculate the IDF score for the current word and store it in the idf_scores dictionary
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
        with open(os.path.join(directory, file), 'r',encoding='utf-8') as f:
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


################### Part 3 : Features to be developed  #####################




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




def words_mentioned_by_all_presidents(tf_idf_matrix):
    all_presidents_words = set(tf_idf_matrix.keys())
    unimportant_words = {word for word, scores in tf_idf_matrix.items() if all(score == 0 for score in scores)}
    important_words = all_presidents_words - unimportant_words
    print("Words Mentioned by All Presidents (excluding 'unimportant' words):", list(important_words))







def extract_words_from_question(question_text):
    # Split the input text into words
    words = question_text.split()
    return words


def identify_corpus_terms(matrix,txt):
    keys_utf8 = []
    answer = []
    for key,values in matrix.items():
        keys_utf8.append(key)

    txt = extract_words_from_question(txt)
    for element in txt:
        if element in keys_utf8:
            answer.append(element)
    return answer

def TF_question(question):
    word_counts = {}
    question_tokens = question.split()
    for element in question_tokens:
        n = word_counts.get(element, 0)
        word_counts[element] = n + 1
    return word_counts


def calculate_tfidf_of_question(tf, idf_scores):
    tfidf_vector = {word: tf[word] * idf_scores.get(word, 0) for word in tf}
    return list(tfidf_vector.values())

# Implement the remaining functions for Part 2

# Function 18a: Scalar product (dot function)
def dot_product(vector1, vector2):
    return sum(x * y for x, y in zip(vector1, vector2))

# Function 18b: Norm of a vector
def vector_norm(vector):
    return math.sqrt(sum(x**2 for x in vector))

# Function 18c: Calculating similarity
def calculate_similarity(vector1, vector2):
    dot = dot_product(vector1, vector2)
    norm_vector1 = vector_norm(vector1)
    norm_vector2 = vector_norm(vector2)

    if (norm_vector1 * norm_vector2) == 0:
        return 0

    similarity = dot / (norm_vector1 * norm_vector2)
    return similarity

# Function 19: Finding the most relevant document
def find_most_relevant_document(tfidf_matrix, question_vector, file_names):
    max_similarity = -1
    most_relevant_document = None

    for doc_vector, file_name in zip(tfidf_matrix.values(), file_names):
        similarity = calculate_similarity(question_vector, doc_vector)
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_document = file_name

    return most_relevant_document

def find_highest_tfidf_word(tfidf_vector, document, question):
    filepath = os.path.join("speeches", document)
    words = question.split()  # You missed the parentheses here

    # Create a dictionary with words from the question and their corresponding TF-IDF values
    tfidf_vectorz = {words[i]: tfidf_vector[i] for i in range(len(words))}  # Use len(words) to get the correct range

    # Sort the dictionary by TF-IDF values in descending order
    sorted_tfidf = sorted(tfidf_vectorz.items(), key=lambda item: item[1], reverse=True)

    with open(filepath.replace("speeches", "cleaned"), 'r', encoding='utf-8') as file:
        document_content = file.read().split()

    for word, _ in sorted_tfidf:
        if word in document_content:
            return word

    return None




def extract_passage_with_word(document, word):
    filepath = os.path.join("speeches", document)
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()
        sentences = text.split(".")
        for i, sentence in enumerate(sentences):
            if word.lower() in [w.strip().lower() for w in sentence.split()]:
                start_index = max(0, i - 1)
                end_index = min(len(sentences), i + 2)
                passage = ".".join(sentences[start_index:end_index]).strip()
                return passage + '.'
    return None

def detect_question_starter(question):
    question_starters = {
        "Comment": "Après analyse, ",
        "Pourquoi": "Car, ",
        "Peux-tu": "Oui, bien sûr!",
        "Quand": "À ce moment-là, ",
        "Où": "Là où, ",
        "Est-ce que": "En effet, ",
        "Quoi": "En ce qui concerne cela, ",
        "Qui": "Quant à la personne en question, ",
        "Combien": "Le nombre est de, ",
        "Pour": "Dans le but de, "
    }
    words = question.split()

    for word in words:
        if word in question_starters:
            return question_starters.get(word)
    return "Comme le dit"



def menu():
    print("######  Hello and welcome to the python project of Rayan Boumedine and Léo Carrouge !  #########")


    print("###################1. Take a Look at our function ##############################################")
    print("###################2. Ask question to our chatbot ############################################# ")

    choice1= int(input("Enter a number of the function you want to execute: "))

    if choice1 == 1:

        print("1. Extract President's First Name")
        print("2. List of President's Last Names")
        print("3. Clean and Remove Punctuation from Speeches")
        print("4. Calculate TF-IDF Matrix")
        print("5. List of Least Important Words")
        print("6. Word with Highest TF-IDF Sum")
        print("7. Most Repeated Word by President")
        print("8. President Speaking about 'Nation'")
        print("9. First President to Mention a Topic")
        print("10. Words Mentioned by All Presidents")

        choice = input("Enter the number of the function you want to execute: ")

        if choice == "1":
            file_name = str(input("enter a name of file ( for exemple : Nomination_Hollande.txt ) :"))
            result = Extract_the_names_of_the_presidents(file_name)
            print("President's First Name:", FstName(result))

        elif choice == "2":
            print("List of President's Last Names:", LofNames(president_names))

        elif choice == "3":
            FCleaner()
            print("Speeches cleaned and punctuation removed.")

        elif choice == "4":
            tfidf_matrix = tfidf("Cleaned")
            print("TF-IDF Matrix:", tfidf_matrix)

        elif choice == "5":
            unimportant_words = least_important_words(tfidf("Cleaned"))
            print("List of Least Important Words:", unimportant_words)

        elif choice == "6":
            highest_tfidf_word = highest_tfidf_words_sum("Cleaned")
            print("Word with Highest TF-IDF Sum:", highest_tfidf_word)

        elif choice == "7":
            president_name = input("Enter the President's last name (e.g., 'Chirac'): ")
            most_repeated_word = repeat_word("Cleaned", president_name)
            print(f"Most Repeated Word by {president_name}:", most_repeated_word)

        elif choice == "8":
            president_max_freq = presidents_speaking_nation("Cleaned")
            print(f"President Speaking Most about 'Nation': {president_max_freq}")

        elif choice == "9":
            topic = input("Enter the topic (for this question it should be climat or ecologie)9: ")
            first_mention = first_president_to_mention_topic("Cleaned", topic)
            print(f"First President to Mention {topic}: {first_mention}")
        elif choice == "10":
            print(words_mentioned_by_all_presidents(tfidf("Cleaned")))

        else:
            print("Invalid choice. Please enter a number between 1 and 10.")

    if choice1 == 2:
        while True:

            filesname = [
            "Nomination_Chirac1.txt",
            "Nomination_Chirac2.txt",
            "Nomination_Giscard dEstaing.txt",
            "Nomination_Hollande.txt",
            "Nomination_Macron.txt",
            "Nomination_Mitterrand1.txt",
            "Nomination_Mitterrand2.txt",
            "Nomination_Sarkozy.txt",
        ]


            question = str(input("##################### Ask a question to Our Chatbot :                       "))
            if AttributeError == True:
                print("Veillez saisir quelque chose dans le thème des discours des présidents !")
            fctA = extract_words_from_question(question)
            fctB = identify_corpus_terms(tfidf("Cleaned"),question)
            tf = TF_question(question)
            tfidf_question = calculate_tfidf_of_question(tf,idf_count("Cleaned"))
            document = find_most_relevant_document(tfidf("Cleaned"),tfidf_question,filesname)
            highest = find_highest_tfidf_word(tfidf_question,document,question)
            final_answer = detect_question_starter(question) +", "+ "comme le dit "+Extract_the_names_of_the_presidents(document)+", " +extract_passage_with_word(document,highest)
            print(final_answer)
            redo = int(input("Type 1 if you wanna send him another question or type 0 if you want to leave : "))
            if redo == 0:
                print("Thank you for using us !")
                break
            else:
                True






menu()



