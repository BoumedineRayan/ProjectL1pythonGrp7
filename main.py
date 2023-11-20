
import os


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
    cleaned_dir = " Cleaned" # Set the name of the directory as "Cleaned"
    if not os.path.exists(cleaned_dir):
        os.mkdir(cleaned_dir) # Create the directory


    # Iterate on the dictionary
    for filename in filenames:
        inputpath = os.path.join("speeches", filename) # Construct a path to the original file in the "speeches" directory
        outputpath = os.path.join(cleaned_dir, filename) # constructs the o,
        # which is the path where the cleaned file will be saved

        with open(inputpath, "r") as inputfile:
            contentofthefile = inputfile.read().lower() # convert to lower case
        with open(outputpath, "w") as outputfile:
            outputfile.write(contentofthefile)     # write the converted text into a new document
            # in the Cleaned directory

FCleaner()
