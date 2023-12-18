import math
import os
import time

president_dict = {
    "Chirac": "Jacques",
    "Giscard dEstaing": "Valéry",
    "Hollande": "François",
    "Macron": "Emmanuel",
    "Mitterrand": "François",
    "Sarkozy": "Nicolas"}


def list_of_files(directory, extension):
    files_names = []
    file_list = os.listdir(directory)
    for filename in file_list:
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


directory = "speeches"
files_names = list_of_files(directory, "txt")


def tf(file_path=None, chaine=None):
    ''' chemin d'accès, str → dict
    Permet de compter le nombre d'occurence d'un fichier,
    ou d'une chaine si file_path est égal à None'''

    if file_path != None: # si l'on veut le tf d'un fichier
        with open(file_path, "r", encoding='utf-8') as file:
            words = file.read().split()
    if chaine != None: # si l'on veut le tf d'une chaine
        words = chaine.split()

    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


def idf(directory):
    ''' repertoire → dict
    Retourne le score idf des mots présents dans le corpus directory'''
    term_count = {}
    total_documents = len(directory)
    for file_name in directory:
        with open(os.path.join("cleaned", file_name), "r", encoding='utf-8') as file:
            terms = set(file.read().split())

        for term in terms:
            if term in term_count: # relève la fréquence d'un terme dans le corpus
                term_count[term] += 1
            else:
                term_count[term] = 1
    idf_scores = {}

    for term, count in term_count.items():
        idf_scores[term] = math.log(total_documents / count)
    return idf_scores


def tfidf(directory):
    ''' repertoire → list(dict)
    Retourne le score tfidf des mots dans chaque
     document du corpus directory'''
    cleaned_directory = os.path.join(os.getcwd(), "cleaned")
    files = list_of_files(cleaned_directory, ".txt")
    idf_scores = idf(files)
    tfidf_matrix = []
    for file_name in files:
        file_path = os.path.join(cleaned_directory, file_name)
        tf_scores = tf(file_path)
        tfidf_dict = {term: tf * idf_scores[term] for term, tf in tf_scores.items()}
        tfidf_matrix.append(tfidf_dict)
    return tfidf_matrix


def mots_chirac():
    ''' Entrée : None → Sortie : str
    Retourne le mot le plus répété par le président Chirac'''
    d1 = tf('cleaned/Nomination_Chirac1.txt')
    d2 = tf('cleaned/Nomination_Chirac2.txt')

    for i in d2: # fusion des 2 dictionnaires ainsi que de leurs clés
        if i not in d1:
            d1[i] = d2[i]
        else:
            d1[i] = d1[i] + d2[i]

    L = []
    for i in d1.items(): L.append(i[1]) # ajout du nombre d'occurence total dans les 2 textes

    maxi = 0
    for i in L:  # repère le maximum de la liste
        if i > maxi: maxi = i

    for i in d1: # on regarde quel mot correspond à la valeur maxi trouvée
        if d1[i] == maxi: return i


def score_tfidf_max(matrice):
    '''Entrée : list(list) → Sortie : str
    Retourne le mot de la matrice avec le score tfdf
    le plus élevé'''
    L = []
    for i in range(len(matrice)): # ajoute toutes les clés de la matrice dans une liste
        for j in matrice[i].items(): L.append(j[1])

    maxi = 0
    for i in L : # repère le maximum de la liste
        if i > maxi : maxi = i

    for i in range(len(matrice)): # retourne le mot qui a pour clé 'maxi'
        for j in matrice[i]:
            if matrice[i][j] == maxi: return j


def mots_non_importants():
    '''Entrée : None → Sortie : None
    Affiche les mots qui ont un idf nul, càd qui ont un score tfidf nul dans tous les docs'''
    mots_doc = set()
    for value in files_names:
        with open(f"cleaned/{value}", "r", encoding='utf-8', errors='ignore') as f:
            mot = f.read().split()
            for mots in mot: mots_doc.add(mots)
    print('\n')
    nb_char = 0
    for mot in mots_doc:
        if idf(files_names)[mot] == 0:
            if nb_char == 0 :
                print('                     ',end='')
            print('«', mot, '»', end=', ')
            time.sleep(0.1)
            nb_char += len(
                mot) + 6  # +6 en comptant les 2 guillemts, la virgule, les 2 esapaces entre les guillemets et le mot et l'espace après la virgule
        if nb_char >= 90: print(); nb_char = 0  # si le nombre de charactère sur une ligne dépasse 85, on revient à ligne
    print('\n')


files_list = list_of_files('cleaned', "txt")


def pres_nation():
    '''Entrée : None → Sortie : list
    Retourne le nom des présidents qui ont parlé de la nation'''
    L = []
    for file in files_list:
        if 'nation' in tf(f'cleaned/{file}'): L.append(file)
    pres = []
    for i in L:
        nom = i.split('.')[0].split('_')[1]
        if '1' in i or '2' in i: # si le président à un chiffre dans le nom de son doc, alors on l'enlève
            for j in president_dict:
                prénom = president_dict[nom[:-1]]
                pres.append(prénom + ' ' + nom[:-1])
        else:
            for j in president_dict:
                prénom = president_dict[nom]
                pres.append(prénom + ' ' + nom)


    return list(set(pres))


def pres_nation_max():
    '''Renvoie le nom du président qui a le plus parlé de la nation '''

    d = {}
    pres = pres_nation()
    for file in files_list :
        d1 = tf(f'cleaned/{file}')
        if 'nation' in d1:
            d[file] = d1['nation']
    max = 0
    for i in d:
        if d[i] > max: max = d[i] # on relève la plus grande clé du dictionnaire
    for i in d:
        if d[i] == max: # on relève le nom du président qui correspond à la valeur max trouvée
            if '1' in i or '2' in i:
                return (i.split('.')[0].split('_')[1])[:-1] # affiche uniquement le nom du président
            else:
                return i.split('.')[0].split('_')[1]


def pres_climat():
    ''' Entrée : None → Sortie : list
    Affiche le nom des présidents qui ont parlé du climat'''
    L = []
    for file in files_names:
        with open(f"cleaned/{file}", "r", encoding='utf-8', errors='ignore') as f:
            mots_doc = f.read().split()
            for mot in mots_doc :
                if 'climat' in mot or 'écologie' in mot :
                    if '1' in file or '2' in file :  nom = file.split('.')[0].split('_')[1][:-1]
                    else : nom = file.split('.')[0].split('_')[1]
                    pres = president_dict[nom] + ' ' +  nom
                    L.append(pres)

    L = list(set(L))
    for i in L :
        if i == L[-2] : print(i,end=' et ')
        elif i == L[-1] : print(i,end=' ')
        else : print(i,end=', ')
        time.sleep(0.1)


def affichage_chaine(chaine):
    '''Entrée: str → Sortie: None
    Affiche la chaine avec un temps d'attente entre chaque mot'''
    chaine = chaine.split()
    nb_char = 0
    for i in chaine:
        if nb_char == 0 :
            print('                     ', end='')
        print(i, end=' ')
        nb_char += len(i) + 1
        if nb_char >= 90: nb_char = 0; print() # si le nombre de caractères sur une ligne dépasse 90, on revient à la ligne
        time.sleep(0.1)


def mots_communs():
    '''Entrée: None → Sortie: None
    Affiche les mots cités par tous les présidents'''

    mandat_unique = [i for i in files_names if '1' not in i and '2' not in i]
    chirac = [i for i in files_names if 'Chirac' in i]
    mitterrand = [i for i in files_names if 'Mitterrand' in i]

    mots1 = [mot for value in mandat_unique for mot in set(open(f"cleaned/{value}", "r", encoding='utf-8').read().split())] # on ajoute tous les mots des présidents n'ayant fait qu'un seul mandat
    mots2 = [mot for value in mitterrand for mot in set(open(f"cleaned/{value}", "r", encoding='utf-8').read().split())] # on ajoute tous les mots cités par Mitterrand
    mots3 = [mot for value in chirac for mot in set(open(f"cleaned/{value}", "r", encoding='utf-8').read().split())] # on ajoute tous les mots cités par Chirac


    mots_communs1 = list(set([i for i in mots1 if mots1.count(i) == len(mandat_unique) and idf(files_names)[i] != 0])) # on ajoute tous les mots présents dans tous les documents des présidents n'ayant fait qu'un seul mandat
    mots_communs2 = list(set([i for i in mots2 if idf(files_names)[i] != 0])) # on ajoute que les mots importants
    mots_communs3 = list(set([i for i in mots3 if idf(files_names)[i] != 0])) # on ajoute que les mots importants

    print('\n')
    nb_char = 0
    for i in mots_communs1:
        if i in mots_communs2 and i in mots_communs3:
            if nb_char == 0:
                print('                     ', end='')
            print('«', i, '»', end=', ')
            nb_char += len(i) + 6
            if nb_char >= 85: print();nb_char = 0
            time.sleep(0.1)



def tok(q):
    a = ""
    L = q.split()
    for mots in L:
        i = 0
        for lettre in mots:
            code_ascii = ord(lettre)
            if 65 <= code_ascii <= 90:
                code_ascii += 32
                a += chr(code_ascii)
            elif 0 <= code_ascii <= 47 or 58 <= code_ascii <= 64 or 91 <= code_ascii <= 96 or 123 <= code_ascii <= 127:
                a += " "
            else:
                a += mots[i]
            i += 1
        if a[-1] != ' ': a += ' '
    return a


def corpus_et_question(q):
    '''Entrée: str → Sortie: list
    Affiche les mots présents dans q et dans le corpus'''
    mots_quest = q.split()
    L = []
    for i in mots_quest:
        for file in files_list:
            if i in tf(f'cleaned/{file}'): L.append(i)
    return list(set(L))


def produit_scalaire(v1, v2):
    '''Entrée: dictionnaire/list, dictionnaire/list → Sortie: int
    Retourne le produit scalaire de v1 et v2'''
    assert len(v1) == len(v2)
    p_scalaire = 0
    for i in range(len(v1)):  p_scalaire += v1[i] * v2[i]
    return p_scalaire


def norme_vecteur(v1):
    '''Entrée : dictionnaire/list →Sortie : float'
    Retourne la norme de v1'''
    for i in range(len(v1)): # on remplace les valurs de v1 par leur carré
        v1[i] = v1[i] ** 2
    somme = 0
    for i in v1: somme += i # on calcule la somme des carrés
    return math.sqrt(somme)

def similarité(v1, v2):
    '''Entrée: dictionnaire/list,dictionnaire/list → Sortie: float'''
    return produit_scalaire(v1, v2) / (norme_vecteur(v1) * norme_vecteur(v2))

def génération(mot):
    '''Entrée: str -> Sortie: str
    Génere la réponse à la question'''
    #mot = score_tfidf_max(tf_idf_question)
    #d_pertient = doc_pertinent

    with open(os.path.join("speeches", 'Nomination_Macron.txt'), "r", encoding='utf-8') as f:
        phrases = f.read().split('.') # on sépare le doc par phrase
    for i in phrases : # on n'affiche que la première phrase
        if mot in i :
            return affichage_chaine(i)


def affiner(q):
    '''Entrée: str -> Sortie: list
    Améliore la qualité de la réponse'''
    question_starters = {
        "Comment": "Après analyse, ",
        "Pourquoi": "Il semblerait que, ",
        "Peux-tu": "Oui, bien sûr !",
        "Explique-moi": "Très bien, "}
    question = q.split()
    for i in question_starters :
        if question[0] == i :
            return question_starters[i]


def mots_question (q):
    letter_list=list(q)
    letter_list_cleaned=[]
    last_element = ""
    for element in letter_list:
        #on convertit chq lettre majuscule en minuscule
        if 65<=ord(element)<=90:
            letter_list_cleaned.append(chr(ord(element)+32))
            last_element=chr(ord(element)+32)
        #on réecrit chq minuscule dans la liste clean
        elif 97<=ord(element)<=122:
            letter_list_cleaned.append(element)
            last_element = element
        #on convertit chq caractère spécial en espace
        else:
            #on vérifie qu'il n'y ai pas deux espaces à la suite
            if last_element!=" ":
                letter_list_cleaned.append(" ")
                last_element = " "
   #on chaque élément de la liste
    j= "".join(letter_list_cleaned)
   #on sépare la chaine de caractère à partir des espaces
    j = j.split(" ")


    L=q.split(" ")
    return j

