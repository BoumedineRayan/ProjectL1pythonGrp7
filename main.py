def extract(file):   # function 1
    with open(file,"r") as f:
        d = {"Nomination_Chirac1.txt":"chirac", "Nomination_Chirac2.txt":"chirac",
             "Nomination_Giscard dEstaing.txt": "Giscard dEstaing", "Nomination_Hollande.txt":"Hollande",
             "Nomination_Macron.txt":"Macron", "Nomination_Mitterrand1.txt":"Mitterand",
             "Nomination_Mitterrand2.txt":"Mitterand", "Nomination_Sarkozy.txt": "Sarkozy"}
        return d(file)

print(extract("Nomination_Mitterrand2.txt"))