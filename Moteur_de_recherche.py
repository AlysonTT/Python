#Partie 2 : TD7
'''
import Corpus
import TPs

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Etape 1 : demander a l’utilisateur d’entrer quelques mots-clefs

mot_clef = input("Entrer vos mots clefs : ") #voir si sil faut préciser de les séparer d'un espaces ou faire une boucle à voir

#Etape 2 : transformer ces mots-clefs sous la forme d’un vecteur sur le vocabulaire précédedemment construit

vectorizer = CountVectorizer() # conversion des document en vecteur
mot_clef_vecteur = vectorizer.transform([mot_clef]) #transforme les clefs en vecteur
corpus = Corpus() # ATTENTION def corpus ==> mieux le faire
corpus_vecteur = vectorizer.transform([corpus])

#Etape 3 : calculer une similarité entre votre vecteur requete et tous les documents

similarite = cosine_similarity(corpus_vecteur, mot_clef_vecteur).flatten() #.flatten va créer une à liste des scores de similarité plus facile à traiter

#Etape 4 : trier les scores resultats et afficher les meilleurs resultats

resultat = [(index, score) for index, score in enumerate(corpus_vecteur)]
resultat.sort()
meilleur_resultat = 3
for i in range (meilleur_resultat) :
    print(resultat[i])
    '''

'''
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from TPs import *
from Corpus import Corpus 

# Charger le corpus depuis le fichier
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

# Etape 1 : demander à l'utilisateur d'entrer quelques mots-clefs
mots_clefs = input("Entrez quelques mots-clés (séparés par des espaces) : ").split()

# Utiliser la méthode creer_vocabulaire pour obtenir le vocabulaire
_, _, vocabulaire_corpus, _, _, _ = corpus.creer_vocabulaire()

# Etape 2 : transformer ces mots-clefs sous la forme d’un vecteur sur le vocabulaire précédemment construit
vectorizer = CountVectorizer(vocabulary=vocabulaire_corpus)  # Conversion des documents en vecteur
mots_clefs_vecteur = vectorizer.transform([" ".join(mots_clefs)])  # Transforme les clefs en vecteur

# Etape 3 : calculer une similarité entre votre vecteur requête et tous les documents
corpus_texte = [doc.texte for doc in corpus.id2doc.values()]  # Liste de textes des documents du corpus
corpus_vecteur = vectorizer.transform(corpus_texte)  # Transforme les textes des documents du corpus en vecteur

similarite = cosine_similarity(corpus_vecteur, mots_clefs_vecteur).flatten()  # .flatten va créer une liste des scores de similarité plus facile à traiter

# Récupération des indices et scores de similarité
resultat = [(index, score) for index, score in enumerate(similarite)]
resultat.sort(key=lambda x: x[1], reverse=True)  # Tri par score de similarité décroissant

# Affichage des meilleurs résultats
meilleur_resultat = 3  # Vous pouvez ajuster le nombre de meilleurs résultats à afficher
for i, (index, score) in enumerate(resultat[:meilleur_resultat]):
    if index in corpus.id2doc:
        document = corpus.id2doc[index]

        print(f"Résultat {i + 1}:")
        print(f"Index du document: {index}")
        print(f"Score de similarité: {score}")
        print(f"Titre du document: {document.titre}")
        print(f"Contenu du document: {document.texte[:100]}...")  # Afficher les 100 premiers caractères du texte
        print("=" * 50)
        # Ajout pour afficher tous les corpus avec les mots-clés
        mots_clefs_present = []
        for mot_clef in mots_clefs:
            if mot_clef in document.texte.lower():
                mots_clefs_present.append(mot_clef)

        if mots_clefs_present:
            print(f"Mots-clés présents dans le document: {', '.join(mots_clefs_present)}")
        else:
            print("Aucun des mots-clés n'est présent dans le document.")
        print("=" * 50)
    else:
        print(f"Document avec l'index {index} non trouvé dans le corpus.")
        '''

import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Vérification de l'importation du module Corpus
try:
    from Corpus import Corpus
    #print("Importation du module Corpus réussie.")
except ImportError:
    print("Échec de l'importation du module Corpus.")

# Vérification de l'importation du module TPs
try:
    from TPs import *
    #print("Importation du module TPs réussie.")
except ImportError:
    print("Échec de l'importation du module TPs.")


# Charger le corpus depuis le fichier
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)
    #print("CORPUS",corpus)

while True:
    # Etape 1 : demander à l'utilisateur d'entrer quelques mots-clefs
    mots_clefs = input("Entrez quelques mots-clés (séparés par des espaces) : ").split()

    # Vérifier si l'utilisateur souhaite quitter
    if 'q' in [mot.lower() for mot in mots_clefs]:
        print("Merci d'avoir utilisé le moteur de recherche. Au revoir!")
        break

    # Utiliser la méthode creer_vocabulaire pour obtenir le vocabulaire
    _, _, vocabulaire_corpus, _, _, _ = corpus.creer_vocabulaire()

    # Etape 2 : transformer ces mots-clefs sous la forme d’un vecteur sur le vocabulaire précédemment construit
    vectorizer = CountVectorizer(vocabulary=vocabulaire_corpus)  
    mots_clefs_vecteur = vectorizer.transform([' '.join(mots_clefs)])

    # Etape 3 : calculer une similarité entre votre vecteur requête et tous les documents
    corpus_texte = [doc.texte for doc in corpus.id2doc.values()]
    corpus_vecteur = vectorizer.transform(corpus_texte)
   
    similarite = cosine_similarity(corpus_vecteur, mots_clefs_vecteur).flatten()
    '''
    # Etape 4 : trier les scores résultats et afficher les meilleurs résultats
    resultat = [(index, score) for index, score in enumerate(similarite)]
    resultat.sort(key=lambda x: x[1], reverse=True)  

    # Affichage des meilleurs résultats uniquement si le mot est trouvé dans le corpus
    if all(score == 0 for _, score in resultat):
        print("Aucun résultat trouvé dans le corpus.")
    else:
        meilleur_resultat = min(3, len(resultat))  
        for i in range(meilleur_resultat):
            index, score = resultat[i]

            print(f"Résultat {i + 1}:")
            print(f"Index du document: {index}")
            if index < len(corpus_texte):
                document_texte = corpus_texte[index]
                print(f"Score de similarité: {score}")
                #print(f"Contenu du document: {document_texte[:100]}...")
                print(f"Contenu du document:\n{document_texte}")
                print("=" * 50)

            else:
                print(f"Document avec l'index {index} non trouvé dans le corpus.")
                '''
    
    '''
    # Afficher les documents qui contiennent au moins un mot-clé
    documents_retrouves = []
    for index, document in corpus.id2doc.items():
        if any(mot.lower() in document.texte.lower() for mot in mots_clefs):
            documents_retrouves.append((index, document))

    if not documents_retrouves:
        print("Aucun résultat trouvé dans le corpus.")
    else:
        print("Résultats trouvés :")
        for i, (index, document) in enumerate(documents_retrouves):
            print(f"Résultat {i + 1}:")
            print(f"Index du document: {index}")
            print(f"Titre du document: {document.titre}")
            print(f"Contenu du document:\n{document.texte}")
            print("=" * 50)
            '''
        # Afficher les documents qui contiennent au moins un mot-clé
    documents_retrouves = []
    for index, document in corpus.id2doc.items():
        if any(mot.lower() in document.texte.lower() for mot in mots_clefs):
            score_document = similarite[index]
            documents_retrouves.append((document, score_document))

    if not documents_retrouves:
        print("Aucun résultat trouvé dans le corpus.")
    else:
        print("Résultats trouvés :")
        for i, (document, score_document) in enumerate(documents_retrouves):
            print(f"Résultat {i + 1}:")
            print(f"Titre du document: {document.titre}")
            print(f"Contenu du document:\n{document.texte}")

            # Afficher le score de similarité pour chaque document
            print(f"Score de similarité: {score_document}")
            print("=" * 50)
