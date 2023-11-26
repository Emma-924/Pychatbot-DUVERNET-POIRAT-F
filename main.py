import os
import math
from Fonctions import *

# Call of the function
directory = "speeches"
files_names = list_of_files(directory, "txt")

L = []
# parcourir la liste
for elements in files_names:
    elements = elements[11:]  # on ne lit pas Nomination_
    elements = elements[:-4]  # on ne lit pas .txt
    if "0" <= elements[-1] <= "9":  #
        elements = elements[:-1]
    if elements not in L:  # Si nom deux fois on en garde un seul
        L.append(elements)

# création d'un dictionnaire pour ajouter à chq nom le prénom correspondant
president_dict = {
    "Chirac": "Jacques",
    "Giscard dEstaing": "Valéry",
    "Hollande": "François",
    "Macron": "Emmanuel",
    "Mitterrand": "François",
    "Sarkozy": "Nicolas"}

for elements in L:
    firstname = president_dict[elements]

file_list = os.listdir("speeches")
# on va convertir chaque caractère majuscule en caractère minuscule
for value in files_names:
    with open(f"speeches/{value}", "r", encoding='utf-8', errors='ignore') as f, open(f"cleaned/c_{value}", "w+",
                                                                                      encoding='utf-8',
                                                                                      errors='ignore') as f2:
        last_element_written = ""
        for line in f:
            for character in line:
                code_ascii = ord(character)
                if 65 <= code_ascii <= 90:
                    code_ascii += 32
                    f2.write(chr(code_ascii))
                    last_element_written = chr(code_ascii)
                # on va modifier tous les caractères qui ne sont pas des lettres en espace
                elif 0 <= code_ascii <= 64 or 91 <= code_ascii <= 96 or 123 <= code_ascii <= 127:
                    if last_element_written != " ":
                        f2.write(" ")
                        last_element_written = " "
                # on va réecrire dans le nouveau fichier toutes les lettres qui étaient déjà en minuscules
                else:
                    f2.write(character)
                    last_element_written = character




for value in files_names:
    with open(f"cleaned/c_{value}", "r", encoding='utf-8', errors='ignore') as f:
        #print(tf(f))
        pass
#print(idf(files_names))


question = int(input('Saisir le numéro de la qustion : '))

if question == 1 :
    print('Les mots les moins importants sont',mots_non_importants())
elif question == 2 :
    pass
elif question == 3 :
    print('Le mot le plus répété par le président Jacques Chirac est',mots_chirac())
elif question == 4 :
    print('Les présidents qui ont parlé de la nation sont',pres_nation())
    print('Le président qui en a le plus parlé est',pres_nation_max())






