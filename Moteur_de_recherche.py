#Partie 2 : TD7

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