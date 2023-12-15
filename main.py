import os
import math
from fonctions import *
import time

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
    with open(f"speeches/{value}", "r", encoding='utf-8', errors='ignore') as f, open(f"cleaned/{value}", "w+",
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


print('\n------------------------------------------ Bienvenue ------------------------------------------ ')
choix = ''
print('1- Connaitre la liste des mots les moins importants')
time.sleep(0.4)
print('2- Connaitre le mot avec le score tf-idf le plus élevé')
time.sleep(0.4)
print('3- Connaitre le mot le plus répété par le président Chirac')
time.sleep(0.4)
print('4- Connaitre la liste des présidents qui ont parlé de la nation et savoir qui en a le plus parlé')
time.sleep(0.4)
print('5- Connaitre le nom du premier président à avoir palé du climat')
time.sleep(0.4)
print('6- Connaitre la liste des mots cités par tous les présidents')
time.sleep(0.4)
print('')
question = input(" --------- Pour accéder au menu des questions,veuillez saisir le numéro d'une question --------- "
                 "\n------------------- Pour accéder au Chatbot, veuillez saisir votre question -------------------\n")

while True:
    if question == '1' :
        affichage_chaine('Les mots les moins importants sont')
        mots_non_importants()
    elif question == '2' :
        affichage_chaine('Le mot avec le score tf-df le plus élevé est')
        print('«', score_tfidf_max(tfidf("cleaned")),'»')
    elif question == '3' :
        affichage_chaine('Le mot le plus répété par le président Jacques Chirac est')
        print('«',mots_chirac(),'»')
    elif question == '4' :
        affichage_chaine ('Les présidents qui ont parlé de la nation sont ')
        for i in pres_nation() :
            if i != pres_nation()[-1] :
                print(i, end=', ')
                time.sleep(0.1)
            else: print('et', i)
        time.sleep(0.1)
        affichage_chaine('Le président qui en a le plus parlé est ')
        print(president_dict[pres_nation_max()],end=' ')
        time.sleep(0.1)
        print(pres_nation_max())
    elif question == '5' :
        affichage_chaine('Le premier président à avoir parlé du climat est')
        print(president_dict[pres_climat()], end=' ')
        time.sleep(0.1)
        print(pres_climat())
    elif question == '6' :
        affichage_chaine('Les mots cités par tous les présidents et qui ne sont pas considérés comme non importants sont')
        mots_communs()
    else :
        q = question
        génération(q)
    time.sleep(0.7)
    choix = input("\n----------------------------- Tapez « STOP » pour quitter le menu -----------------------------\n------------------------- Pour continuer saisissez une autre question -------------------------\n")
    if choix == 'STOP':
        break
    question = choix


