import time
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


def tf_calculation(f):
    """
    :param f:
    :return: occurences
    """
    file_content = f.read()
    words_list = file_content.split()   # Diviser le texte en mot à partir des espaces
    occurrences = {}
    for word in words_list:
        if word in occurrences:
            occurrences[word] += 1   # Si le mot est déjà dans le dictionnaire, ajouter 1 à sa valeur
        else:
            occurrences[word] = 1   # Si le mot n'est pas déjà dans le dictionnaire, l'ajouter et mettre sa valeur à 1
    return occurrences

def idf_calculation(corpus_dir):
    """
    :param corpus_dir:
    :return: idf
    """
    word_count = {}
    number_of_files = len(os.listdir(corpus_dir))   # Compter le nombre de fichiers
    for file_name in os.listdir(corpus_dir):
        with open(f"{corpus_dir}\\{file_name}", 'r') as f:
            file_content = f.read()
            words_list = file_content.split()   # Diviser le texte en mot à partir des espaces
            unique_words = set(words_list)   # Eliminer les doublons en transformant la liste en set
            for word in unique_words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
    idf = {}
    words = list(word_count.keys())   # Faire une liste avec les clés du dictionnaire
    counts = list(word_count.values())   # Faire une liste avec les valeurs du dictionnaire
    for i in range(len(words)):
        word = words[i]
        count = counts[i]
        idf[word] = math.log10(number_of_files / count)   # Calculer le score IDF et l'enregistrer dans un dictionnaire
    return idf
# calculer les scores TF-IDF
def tfidf_matrix(corpus_dir):
    """
    :param corpus_dir:
    :return: tfidf_matrix
    """
    tfidf_matrix = []
    idf_scores = idf_calculation(corpus_dir)   # Récupérer le score IDF
    for filename in os.listdir(corpus_dir):
        with open(f"{corpus_dir}\\{filename}", 'r') as f:
            tf_scores = tf_calculation(f)   # Récupérer le score TF du document
            tfidf_scores = {}
            for word in tf_scores:
                tf = tf_scores[word]   # Récupérer le score TF du mot dans le document
                idf = idf_scores[word]   # Récupérer le score IDF du mot
                tfidf_scores[word] = tf * idf   # Calculer le score TF-IDF
            tfidf_matrix.append(tfidf_scores)   # Remplir le tableau avec le dictionnaire de scores TF-IDF du document
    return tfidf_matrix

"""----------CORPS DU PROGRAMME PRINCIPAL----------"""

# Obtenir la matrice TF-IDF
tfidf_matrix_result = tfidf_matrix("cleaned")

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
        tf_scores = tf_calculation(file_path)
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
    for value in files_names: # ajoute tous les mots du corpus
        with open(f"cleaned/{value}", "r", encoding='utf-8', errors='ignore') as f:
            mot = f.read().split()
            for mots in mot: mots_doc.add(mots)

    print('\n')
    nb_char = 0
    for mot in mots_doc:
        if idf(files_names)[mot] == 0: # n'affiche que ceux qui ont un idf nul
            if nb_char == 0 :
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
    for file in files_list:
        d1 = tf(f'cleaned/{file}')
        if 'nation' in d1:
            d[file] = d1['nation']
    max = 0
    for i in d:
        if d[i] > max: max = d[i] # on relève la plus grande clé de la liste
    for i in d:
        if d[i] == max: # on relève le nom du président qui correspond à la valeur max trouvée
            if '1' in i or '2' in i:
                return (i.split('.')[0].split('_')[1])[:-1] # affiche uniquement le nom du président
            else:
                return i.split('.')[0].split('_')[1]


ordre = ['Nomination_Giscard dEstaing.txt', 'Nomination_Mitterrand1.txt', 'Nomination_Mitterrand2.txt',
         'Nomination_Chirac1.txt', 'Nomination_Chirac2.txt', 'Nomination_Sarkozy.txt', 'Nomination_Hollande.txt',
         'Nomination_Macron.txt']


def pres_climat():
    ''' Entrée : None → Sortie : list
    Retorune le nom du premier président qui a parlé du climat'''
    L = []
    for file in ordre:
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
        print(i, end=' ')
        nb_char += len(i) + 1
        if nb_char >= 90: nb_char = 0; print() # si le nombre de caractère sur une ligne dépasse 9à, on reviens à la ligne
        time.sleep(0.1)


def mots_communs():
    '''Entrée: None → Sortie: None
    Affiche les mots cité par tous les présidents'''

    mandat_unique = [i for i in files_names if '1' not in i and '2' not in i]
    chirac = [i for i in files_names if 'Chirac' in i]
    mitterrand = [i for i in files_names if 'Mitterrand' in i]

    mots1 = [mot for value in mandat_unique for mot in set(open(f"cleaned/{value}", "r", encoding='utf-8').read().split())] # on ajoute tous les mots des présidents n'ayant fait qu'un seul mandat
    mots2 = [mot for value in mitterrand for mot in set(open(f"cleaned/{value}", "r", encoding='utf-8').read().split())] # on ajoute tous les mots cités par Mitterrand
    mots3 = [mot for value in chirac for mot in set(open(f"cleaned/{value}", "r", encoding='utf-8').read().split())] # on ajoute tous les mots cités par Chirac


    mots_communs1 = list(set([i for i in mots1 if mots1.count(i) == len(mandat_unique) and idf(files_names)[i] != 0])) # on ajoute tous les mots présents dans tous les documents des présidents n'ayant fait qu'un seul mandat
    mots_communs2 = list(set([i for i in mots2 if idf(files_names)[i] != 0])) # on ajoute que les mots importants
    mots_communs3 = list(set([i for i in mots3 if idf(files_names)[i] != 0])) # on ajoute que les mots importants

    nb_char = 0
    print('\n')
    for i in mots_communs1 :
        if i in mots_communs2 and i in mots_communs3 : # on n'affiche que les mots présents dans les 3 documents
            print('«', i, '»', end=', ')
            nb_char += len(i) + 6
            if nb_char >= 90 : print();nb_char =0

    '''L = ['sont', 'm', 'un', 'ont', 'leur', 'avec', 'mai', 'n', 'chacun', 's', 'cette', 'pas', 'lui', 'droits', 'politique', 'sont', 'avenir', 'confiance']
    for value in files_names :
        for i in L :
            with open(f"cleaned/{value}", "r", encoding='utf-8') as f:
                if i not in f.read():
                    print(i, value)'''


# convertir la question en liste de mots
def tokenize_question(question):
    letter_list_cleaned = []
    letter_list = list(question)
    for character in letter_list:
        if 97 <= ord(character) <= 122:
            letter_list_cleaned.append(character)
            last_character = character
        elif 65 <= ord(character) <= 90:
            letter_list_cleaned.append(chr(ord(character) + 32))
            last_character = chr(ord(character) + 32)
        elif 0 <= ord(character) <= 64 or 91 <= ord(character) <= 96 or 123 <= ord(character) <= 127:
            if last_character != " ":
                letter_list_cleaned.append(" ")
                last_character = " "
        else:
            letter_list_cleaned.append(character)
            last_character = character
    while letter_list_cleaned and letter_list_cleaned[-1] == " ":
        del letter_list_cleaned[-1]
    question = "".join(letter_list_cleaned)
    word_list = question.split(" ")
    return word_list


# trouver les mots qui sont dans la question et dans le corpus
def intersection_terms(question_words, corpus_directory):
    question_set = set(question_words)
    corpus = read_documents(corpus_directory)
    corpus_words = []
    for document in corpus:
        for word in document.split():
            corpus_words.append(word)
    corpus_set = set(corpus_words)
    common_terms = question_set & corpus_set
    return list(common_terms)


# calculer le score tfidf de la question
def tfidf_vector(words, idf_scores):
    tf_vector = {}
    question_words = set(words)
    for word in question_words:
        tf = words.count(word) / len(words)
        if word in idf_scores:
            tf_vector[word] = tf * idf_scores[word]
        else:
            tf_vector[word] = 0
        if word == "comment":
            tf_vector[word] = 0
    return tf_vector


# calculer les normes des vecteurs
def norm(vector):
    squared_sum = 0
    for value in vector.values():
        squared_sum += value ** 2
    return math.sqrt(squared_sum)


# calculer la similarité
def cosine_similarity(vector_a, vector_b):
    common_words = set(vector_a.keys()) & set(vector_b.keys())
    if not common_words:
        return 0
    dot_prod = 0
    for word in common_words:
        dot_prod += vector_a[word] * vector_b[word]
    norm_a = norm(vector_a)
    norm_b = norm(vector_b)
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot_prod / (norm_a * norm_b)


# claculer le document le plus pertinent
def most_relevant_document(question_vector, tfidf_matrix, file_names):
    similarities = {}
    for i, document_vector in enumerate(tfidf_matrix):
        similarity = cosine_similarity(question_vector, document_vector)
        similarities[file_names[i]] = similarity
    return max(similarities, key=similarities.get)


# générer une réponse
def generate_response(most_relevant_doc, highest_tfidf_word):
    with open(f"cleaned\\{most_relevant_doc}", 'r') as f:
        document_content = f.read()
        sentences = document_content.split('.')
        for sentence in sentences:
            if highest_tfidf_word in sentence:
                return sentence
    return None


# faire une liste du contenu des fichier textes
def read_documents(directory):
    corpus = []
    for filename in os.listdir(directory):
        with open(f"cleaned\\{filename}", 'r') as f:
            document = f.read()
            corpus.append(document)
    return corpus
