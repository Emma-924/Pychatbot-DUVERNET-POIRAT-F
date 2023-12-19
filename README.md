Aperçu
Ce projet analyse les discours présidentiels pour extraire des informations et répondre à des questions spécifiques liées au contenu des discours. Le code est écrit en Python et utilise diverses fonctions pour le traitement et l'analyse de texte.
Table des matières
•	Configuration
•	Utilisation
•	Questions traitées
•	Structure des fichiers
Configuration
1.	Installation des dépendances :
•	Assurez-vous d'avoir Python installé sur votre machine.
•	Installez les dépendances requises en exécutant pip install -r requirements.txt.
2.	Répertoire des discours :
•	Placez les discours présidentiels dans le répertoire "speeches".
3.	Exécution :
•	Lancez le script principal en exécutant python main_script.py.
Utilisation
En exécutant le script, un menu s'affichera, permettant à l'utilisateur de choisir parmi différentes questions liées aux discours présidentiels. L'utilisateur peut saisir un numéro correspondant à une question spécifique ou entrer 7 pour interagir avec le chatbot.

Questions traitées
1.	Liste des mots non importants :
•	Affiche une liste des mots les moins importants dans les discours.
2.	Mot avec le score TF-IDF le plus élevé :
•	Identifie le mot avec le score TF-IDF le plus élevé dans l'ensemble des discours.
3.	Mot le plus répété par le président Chirac :
•	Trouve le mot le plus souvent répété dans les discours du président Jacques Chirac.
4.	Présidents discutant de la nation :
•	Liste les présidents ayant discuté de la nation et identifie celui qui en a le plus parlé.
5.	Premier président à discuter du climat :
•	Détermine le premier président à avoir discuté du thème du climat.
6.	Mots communs à tous les présidents :
•	Liste les mots mentionnés par tous les présidents, à l'exception des mots non importants.
7.	Interaction avec le Chatbot :
•	Permet à l'utilisateur d'interagir avec le chatbot en posant des questions.




