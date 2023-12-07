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
def tf(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
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
    print('\n')
    nb_char = 0
    for mot in mots_doc:
        if idf(files_names)[mot] == 0:
            print('«',mot,'»', end=', ')
            time.sleep(0.1)
            nb_char += len(mot)+6 # +6 en comptant les 2 guillemts, la virgule, les 2 esapaces entre les guillemets et le mot et l'espace après la virgule
        if nb_char >= 85 : print() ; nb_char = 0 # si le nombre de charactère sur une ligne dépasse 85, on revient à ligne
    print('\n')

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
        if 'nation' in d1:
            d[file] = d1['nation']
    max = 0
    for i in d:
        if d[i] > max: max = d[i]
    for i in d:
        if d[i] == max :
            if '1' in i or '2' in i : return (i.split('.')[0].split('_')[1])[:-1]
            else : return i.split('.')[0].split('_')[1]
ordre = ['Nomination_Giscard dEstaing.txt','Nomination_Mitterrand1.txt','Nomination_Mitterrand2.txt','Nomination_Chirac1.txt','Nomination_Chirac2.txt','Nomination_Sarkozy.txt','Nomination_Hollande.txt','Nomination_Macron.txt']
def pres_climat():
    for file in ordre:
        if 'climat' in tf(f'cleaned/{file}') or 'écologie' in tf(f'cleaned/{file}'): return file.split('.')[0].split('_')[1]

def affichage_chaine(chaine):
    chaine = chaine.split()
    nb_char = 0
    for i in chaine:
        print(i, end=' ')
        nb_char += len(i)+1
        if nb_char >= 85 : nb_char = 0 ; print()
        time.sleep(0.1)

def mots_communs():

    mandat_double = [i for i in files_names if '1' in i or '2' in i ]
    mandat_unique = [i for i in files_names if '1' not in i and '2' not in i]

    mots1 = [mot for value in mandat_double for mot in set(open(f"cleaned/{value}", "r", encoding='utf-8').read().split())]
    mots2 = [mot for value in mandat_unique for mot in set(open(f"cleaned/{value}", "r", encoding='utf-8').read().split())]

    mots_communs1 = set([i for i in mots1 if mots1.count(i) == len(mandat_double) / 2 and idf(files_names)[i] != 0])
    mots_communs2 = set([i for i in mots2 if mots2.count(i) == len(mandat_unique) and idf(files_names)[i] != 0 ])

    '''L = ['mandat', 'où', 'aussi', 'président', 'femmes', 'démocratie','valeurs','action','temps','mai', 'nos', 'jour', 'bien', 'politique', 'me', 'même', 'comme', 'justice', 'vive', 'toujours', 'chaque','c','moi','chacun','au','sur','autres']
    for i in L :
        for value in files_names:
            with open(f"cleaned/{value}", "r", encoding='utf-8') as f:
                if i not in f.read() :
                    if value != 'Nomination_Chirac1.txt' and value != 'Nomination_Chirac2.txt' and value != 'Nomination_Mitterrand1.txt' and value != 'Nomination_Mitterrand2.txt':
                        print(i, value)'''

    print('\n')
    for i in mots_communs1:
        if i in mots_communs2:
            print('«',i,'»', end = ', ')
            time.sleep(0.1)
    print('\n')

def tok(q):
    a = ""
    L = q.split()
    print(L)
    for mots in L :
        i = 0
        for lettre in mots :
            code_ascii = ord(lettre)
            if 65 <= code_ascii <= 90 :
                code_ascii += 32
                a += chr(code_ascii)
            elif 0 <= code_ascii <= 47 or 58 <= code_ascii <= 64 or 91 <= code_ascii <= 96 or 123 <= code_ascii <= 127:
                    a += " "
            else :
                a += mots[i]
            i += 1
        if a[-1] != ' ' : a += ' '
    return a
def corpus_et_question (q):
    mots_quest = q.split()
    L = []
    for i in mots_quest :
        for file in files_list:
            if i in tf(f'cleaned/{file}'): L.append(i)
    print(set(L))
def idf_question(chaine):
    mots = chaine.split()
    d = {}
    for i in mots :
        if i in d : d[i]+=1
        else : d[i]=1
    return d
