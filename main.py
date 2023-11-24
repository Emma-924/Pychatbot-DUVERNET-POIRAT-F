import os
import math


def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


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
print(L)

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
    print(firstname, elements)

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

def tf(chaine_str):
    mots = chaine_str.split()
    compteur_mots = {}
    for mot in mots:
        if mot in compteur_mots:
            compteur_mots[mot] += 1
        else:
            compteur_mots[mot] = 1
    return compteur_mots

def idf(directory):
    termes = {}
    nb_doc = len(directory)
    for value in directory:
        with open(f"cleaned/c_{value}", "r", encoding='utf-8', errors='ignore') as f:
            mots = set(f.read().split())

        for mot in mots:
            if mot in termes:
                termes[mot] += 1
            else:
                termes[mot] = 1
    score_idf = {}
    for mot in termes :
        score_idf[mot] = math.log10(nb_doc / termes[mot])
    return score_idf

for value in files_names:
    with open(f"cleaned/c_{value}", "r") as f:
        print(value, '-->', tf(f.read()))
print((idf(files_names)))


def tfidf(directory):
    tfidfmat=[] # on a initialisé la matrice
    S=idf(directory) #on récupère le score idf
    L=os.listdir(directory) #on remplit une liste avec le nom des documents
    #on crée une boucle qui parcours chaque élement de la liste
    for element in L:
        with open(f"cleaned/{element}", "r") as f: #on ouvre chaque fichier
            tfscore=tf(f) #on récupère le score tf de chaque fichier
            tfidf_dict={}
            for element in tfscore: #boucle qui parcours chaque élement de la matrice tf
                tf= tf[element] #on met dans une variable le score tf de  l'élement
                idf= idf[element]#on fait pareil avec le idf
                tfidf_dict[element]=tf*idf #on multiplie le tf et le idf de chaque élément
            tfidfmat.append(tfidf_dict) #on ajoute le score dans la matrice
    return tfidfmat #permet de retourner la matrice l'orsqu'on appelle la fonction
print(tfidf('cleaned')) # affiche la matrice tfidf



'''
pres = []
for value in files_names:
    with open(f"cleaned/c_{value}", "r", encoding='utf-8', errors='ignore') as f:
        if 'nation' in idf(f.read().split()): pres.append((value))
d={}
for value in pres :
    with open(f"cleaned/c_{value}", "r", encoding='utf-8', errors='ignore') as f:
        d[value] = nb_occ(f.read())['nation']
max = 0
for i in d :
    if d[i]>max:
        max = d[i]
for i in d :
    if d[i] == max :
        print('\n',(i.split('_')[1]).split('.')[0])
'''







