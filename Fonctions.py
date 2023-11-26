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
    term_count = {}
    total_documents = len(directory)
    for file_name in directory:
        with open(os.path.join("cleaned", file_name), "r", encoding='utf-8') as file:
            terms = set(file.read().split())
        for term in terms:
            if term in term_count:
                term_count[term] += 1
            else:
                term_count[term] = 1
    idf_scores = {}
    for term, count in term_count.items():
        idf_scores[term] = math.log(total_documents / count)
    return idf_scores

def tfidf(directory):
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
    with open(f"cleaned/Nomination_Chirac1.txt", "r", encoding='utf-8', errors='ignore') as f:
        d1=tf(f)
    with open(f"cleaned/Nomination_Chirac2.txt", "r", encoding='utf-8', errors='ignore') as f:
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
        with open(f"cleaned/{value}", "r", encoding='utf-8', errors='ignore') as f:
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
        with open(f"cleaned/{value}", "r", encoding='utf-8', errors='ignore') as f:
            if 'nation' in tf(f): L.append(value)
    pres = []
    for i in L:
        '''a = i.split('.')[0].split('_')[1]
        if '1' in a or '2' in a:
            a = a[:-1]
        if a not in pres : pres.append(a)'''
        pres.append(i.split('.')[0].split('_')[1])
    return pres


def pres_nation_max():
    d = {}
    pres = pres_nation()
    for value in pres:
        with open(f"cleaned/Nomination_{value}.txt", "r", encoding='utf-8', errors='ignore') as f:
            d1 = tf(f)
            d[value] = d1['nation']

    # président qui en parle le plus
    max = 0
    for i in d:
        if d[i] > max:
            max = d[i]
    for i in d:
        if d[i] == max:
            if '1' in i or '2' in i :
                return i[:-1]

