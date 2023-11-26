import math
import os

def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

directory = "speeches"
files_names = list_of_files(directory, "txt")
def tf(f):
    contenu = f.read()
    mots = contenu.split()
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
        score_idf[mot] = math.log10((nb_doc / termes[mot]))
    return score_idf

'''def tfidf(directory):
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
    return tfidfmat #permet de retourner la matrice lorsque l'on appelle la fonction
print(tfidf('cleaned')) # affiche la matrice tfidf'''




def mots_chirac():
    with open(f"cleaned/c_Nomination_Chirac1.txt", "r", encoding='utf-8', errors='ignore') as f:
        d1=tf(f)
    with open(f"cleaned/c_Nomination_Chirac2.txt", "r", encoding='utf-8', errors='ignore') as f:
        d2=tf(f)
    d=d1
    for i in d2:
        if i not in d :
            d[i] = d2[i]
        else :
            d[i] = d[i] + d2[i]
    L=[]
    for i in d.items() :
        L.append(i[1])
    maxi = max(L)
    for i in d :
        if d[i] == maxi:
            return i

def mots_non_importants():
    mots_doc = set()
    for value in files_names:
        with open(f"cleaned/c_{value}", "r", encoding='utf-8', errors='ignore') as f:
            mot = f.read().split()
            for mots in mot:
                mots_doc.add(mots)

    m_non_importants = []
    for mot in mots_doc:
        if idf(files_names)[mot] == 0:
            m_non_importants.append(mot)
    return m_non_importants

def pres_nation():
    L = []
    for value in files_names:
        with open(f"cleaned/c_{value}", "r", encoding='utf-8', errors='ignore') as f:
            if 'nation' in tf(f): L.append(value)
    pres = []
    for i in L:
        pres.append((i.split('.')[0]).split('_')[1])
    return pres


def pres_nation_max():
    d = {}
    pres = pres_nation()
    for value in pres:
        with open(f"cleaned/c_Nomination_{value}.txt", "r", encoding='utf-8', errors='ignore') as f:
            d1 = tf(f)
            d[value] = d1['nation']

    # président qui en parle le plus
    max = 0
    for i in d:
        if d[i] > max:
            max = d[i]
    for i in d:
        if d[i] == max:
            return i