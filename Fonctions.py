import math
import os

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
def tf(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        #print("=$$$$=", file_path)
        words = file.read().split()
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    return word_count

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
    d1=tf('cleaned/Nomination_Chirac1.txt')
    d2=tf('cleaned/Nomination_Chirac2.txt')
    for i in d2:
        if i not in d1 : d1[i] = d2[i]
        else : d1[i] = d1[i] + d2[i]
    L=[]
    for i in d1.items() : L.append(i[1])
    maxi = max(L)
    for i in d1 :
        if d1[i] == maxi : return i

def score_tfidf_max():
    L = []
    for i in range(len(tfidf("cleaned"))):
        for j in tfidf("cleaned")[i].items() : L.append(j[1])
    maxi = max(L)
    for i in range(len(tfidf("cleaned"))):
        for j in tfidf("cleaned")[i] :
            if tfidf("cleaned")[i][j]== maxi : return j

def mots_non_importants():
    mots_doc = set()
    for value in files_names:
        with open(f"cleaned/{value}", "r", encoding='utf-8', errors='ignore') as f:
            mot = f.read().split()
            for mots in mot : mots_doc.add(mots)
    m_non_importants = []
    for mot in mots_doc:
        if idf(files_names)[mot] == 0: m_non_importants.append(mot)
    return m_non_importants


files_list = list_of_files('cleaned', "txt")

def pres_nation():
    L = []
    for file in files_list:
        if 'nation' in tf(f'cleaned/{file}'): L.append(file)
    pres = []
    for i in L:
        nom = i.split('.')[0].split('_')[1]
        if ('1' in i or '2' in i ):
            for j in president_dict :
                prénom = president_dict[nom[:-1]]
                pres.append(prénom + ' ' + nom[:-1])
        else:
            for j in president_dict :
                prénom = president_dict[nom]
                pres.append(prénom + ' ' + nom)
    return list(set(pres))


def pres_nation_max():
    d = {}
    pres = pres_nation()
    for file in files_list:
        d1 = tf(f'cleaned/{file}')
        d[file]=0
        if 'nation' in d1:
            d[file] = d1['nation']
    max = 0
    for i in d:
        if d[i] > max: max = d[i]
    for i in d:
        if d[i] == max:
            if '1' in i or '2' in i : return (i.split('.')[0].split('_')[1])[:-1]
            else : return i.split('.')[0].split('_')[1]

def pres_climat():
    for file in files_list:
        if 'climat' in tf(f'cleaned/{file}') or 'écologie' in tf(f'cleaned/{file}'): return file.split('.')[0].split('_')[1]
