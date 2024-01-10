import tkinter as tk
from tkinter import Text, Scrollbar, Entry, Button, Label, messagebox
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Vérification de l'importation du module Corpus
try:
    from Corpus import Corpus
except ImportError:
    print("Échec de l'importation du module Corpus.")

# Charger le corpus depuis le fichier
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

# Variables pour stocker l'état des Checkbuttons
checkbutton_vars = []

# Variables pour stocker l'état des Checkbuttons "Afficher"
checkbutton_vars_afficher = []

# Variables pour stocker l'état des Checkbuttons "Comparer"
checkbutton_vars_comparer = []

#fonction qui permet d'avoir qu'un type de source selectionné
def selection_unique(index):
    for i, var in enumerate(checkbutton_vars):
        if i != index:
            var.set(0)

def checkbutton_selection(variables):
    # Afficher les éléments sélectionnés
    options_selectionnees = [source[i] for i, var in enumerate(checkbutton_vars) if var.get()]
    if options_selectionnees:
        return ", ".join(options_selectionnees)
    else:
        return "null"
'''
def effectuer_recherche(entry_mots_clefs, corpus, variables, zone_texte, selected_source):
    # Récupérer le type de source
    selected_source_type = selected_source.get()
    print(selected_source_type)

    # Etape 1 : obtenir les mots-clefs à partir du champ de texte
    mots_clefs = entry_mots_clefs.get().split()

    # Utiliser la méthode creer_vocabulaire pour obtenir le vocabulaire
    _, _, vocabulaire_corpus, _, _, _ = corpus.creer_vocabulaire()

    # Etape 2 : transformer ces mots-clefs sous la forme d’un vecteur sur le vocabulaire précédemment construit
    vectorizer = CountVectorizer(vocabulary=vocabulaire_corpus)  
    mots_clefs_vecteur = vectorizer.transform([' '.join(mots_clefs)])

    # Etape 3 : calculer une similarité entre votre vecteur requête et tous les documents
    corpus_texte = [doc.texte for doc in corpus.id2doc.values()]
    corpus_vecteur = vectorizer.transform(corpus_texte)
    similarite = cosine_similarity(corpus_vecteur, mots_clefs_vecteur).flatten()

    # Afficher les documents qui contiennent au moins un mot-clé avec le score de similarité
    documents_retrouves = []
    for document, score_document in zip(corpus.id2doc.values(), similarite):
        mots_trouves_texte = all(mot.lower() in document.texte.lower() for mot in mots_clefs)
        mots_trouves_titre = all(mot.lower() in document.titre.lower() for mot in mots_clefs)

        # On cherche les mots clés dans le texte ou dans le titre du document
        if mots_trouves_texte or mots_trouves_titre:           
            if document not in documents_retrouves:
                if selected_source_type == "null" or selected_source_type.lower() in document.url.lower():
                    documents_retrouves.append((document, score_document))
                    print("Document trouvé (texte):", document.titre)
                    print("Score:", score_document)
                    print("Nombre de documents trouvés:", len(documents_retrouves))

    # Trier les résultats par score de similarité
    documents_retrouves.sort(key=lambda x: x[1], reverse=True)

    # Effacer le contenu précédent du widget de texte
    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)

    # Afficher les trois meilleurs résultats (avec score non nul)
    if not documents_retrouves:
        zone_texte.insert(tk.END, "Aucun résultat trouvé dans le corpus.")
    else:
        meilleur_resultat_affiche = 0
        for i, (document, score_document) in enumerate(documents_retrouves):
            if (score_document != 0 or meilleur_resultat_affiche < 3) and (mots_trouves_titre or meilleur_resultat_affiche < 3):
                
                zone_texte.insert(tk.END, f"Résultat {i + 1} :\n", "gras")
                zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", )
                zone_texte.insert(tk.END, f"Contenu du document :\n{document.texte}\n")

                # Mettre en rouge les mots-clés dans le texte du document
                for mot in mots_clefs:
                    start_index = "1.0"
                    while start_index:
                        start_index = zone_texte.search(mot, start_index, tk.END, nocase=True)
                        if start_index:
                            end_index = f"{start_index}+{len(mot)}c"
                            zone_texte.tag_add("rouge", start_index, end_index)
                            start_index = end_index

                zone_texte.insert(tk.END, f"Score de similarité: {score_document}\n")
                zone_texte.insert(tk.END, "=" * 150 + "\n")
                meilleur_resultat_affiche += 1

        # Désactiver la modification de la zone de texte
        zone_texte.config(state=tk.DISABLED)
'''


def effectuer_recherche(entry_mots_clefs, corpus, variables, zone_texte, selected_source, checkbutton_vars_afficher, checkbutton_vars_comparer):
    # Récupérer le type de source
    selected_source_type = selected_source.get()

    # Etape 1 : obtenir les mots-clefs à partir du champ de texte
    mots_clefs = entry_mots_clefs.get().split()

    # Utiliser la méthode creer_vocabulaire pour obtenir le vocabulaire
    _, _, vocabulaire_corpus, _, _, _ = corpus.creer_vocabulaire()

    # Etape 2 : transformer ces mots-clefs sous la forme d’un vecteur sur le vocabulaire précédemment construit
    vectorizer = CountVectorizer(vocabulary=vocabulaire_corpus)
    mots_clefs_vecteur = vectorizer.transform([' '.join(mots_clefs)])

    # Etape 3 : calculer une similarité entre votre vecteur requête et tous les documents
    corpus_texte = [doc.texte for doc in corpus.id2doc.values()]
    corpus_vecteur = vectorizer.transform(corpus_texte)
    similarite = cosine_similarity(corpus_vecteur, mots_clefs_vecteur).flatten()

    # Afficher les documents qui contiennent au moins un mot-clé avec le score de similarité
    documents_retrouves = []
    for document, score_document in zip(corpus.id2doc.values(), similarite):
        mots_trouves_texte = all(mot.lower() in document.texte.lower() for mot in mots_clefs)
        mots_trouves_titre = all(mot.lower() in document.titre.lower() for mot in mots_clefs)

        # On cherche les mots clés dans le texte ou dans le titre du document
        if mots_trouves_texte or mots_trouves_titre:
            if document not in documents_retrouves:
                if selected_source_type == "null" or selected_source_type.lower() in document.url.lower():
                    documents_retrouves.append((document, score_document))

    # Trier les résultats par score de similarité
    documents_retrouves.sort(key=lambda x: x[1], reverse=True)

    # Effacer le contenu précédent du widget de texte
    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)

    boutons_par_document = {}
    boutons_afficher_temp = []  # Liste temporaire pour les Checkbutton Afficher

    # Afficher les trois meilleurs résultats (avec score non nul)
    if not documents_retrouves:
        zone_texte.insert(tk.END, "Aucun résultat trouvé dans le corpus.")
    else:
        for i, (document, score_document) in enumerate(documents_retrouves):
            if (score_document != 0 or i < 3):
                zone_texte.insert(tk.END, f"Résultat {i + 1} :\n", "gras")
                zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", )
                zone_texte.insert(tk.END, f"Contenu du document :\n{document.texte}\n")

                # Mettre en rouge les mots-clés dans le texte du document
                for mot in mots_clefs:
                    start_index = "1.0"
                    while start_index:
                        start_index = zone_texte.search(mot, start_index, tk.END, nocase=True)
                        if start_index:
                            end_index = f"{start_index}+{len(mot)}c"
                            zone_texte.tag_add("rouge", start_index, end_index)
                            start_index = end_index

                zone_texte.insert(tk.END, f"Score de similarité: {score_document}\n")
                zone_texte.insert(tk.END, "=" * 150 + "\n")

                var_afficher = tk.IntVar()
                bouton_check = tk.Checkbutton(zone_texte, text="Afficher", variable=var_afficher, font=("Helvetica", 10),
                                              command=lambda doc=document, var=var_afficher: afficher_details_selectionnes(corpus, checkbutton_vars_afficher, zone_texte))
                bouton_check.document = document
                zone_texte.window_create(tk.END, window=bouton_check)
                zone_texte.insert(tk.END, "\n")

                var_comparer = tk.IntVar()
                bouton_comparer_doc = tk.Checkbutton(
                    zone_texte,
                    text="Comparer", variable=var_comparer, font=("Helvetica", 10),
                    command=lambda doc=document, var=var_comparer: comparer_documents(corpus, checkbutton_vars_comparer, zone_texte))

                bouton_comparer_doc.document = document
                zone_texte.window_create(tk.END, window=bouton_comparer_doc)
                zone_texte.insert(tk.END, "\n")

                boutons_par_document[document] = (var_afficher, var_comparer, score_document)

        # Tri des documents par score après les avoir tous ajoutés
        boutons_afficher_temp = sorted(boutons_par_document.items(), key=lambda x: x[1][2], reverse=True)

        checkbutton_vars_afficher[:] = [var_afficher for _, (var_afficher, _, _) in boutons_afficher_temp]
        checkbutton_vars_comparer[:] = [var_comparer for _, (_, var_comparer, _) in boutons_afficher_temp]

    # Désactiver la modification de la zone de texte
    zone_texte.config(state=tk.DISABLED)

def afficher_details_selectionnes(corpus, checkbutton_vars_afficher, zone_texte):
    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)

    # Récupérer les documents sélectionnés
    documents_selectionnes = [document for document, var in zip(corpus.id2doc.values(), checkbutton_vars_afficher) if var.get()]

    # Afficher les détails des documents sélectionnés
    for document in documents_selectionnes:
        zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", "gras")
        zone_texte.insert(tk.END, f"Auteur du document : {document.auteur}\n")
        zone_texte.insert(tk.END, f"URL du document : {document.url}\n")
        zone_texte.insert(tk.END, f"Contenu du document :\n{document.texte}\n")
        zone_texte.insert(tk.END, "=" * 150 + "\n")

    # Désactiver la modification de la zone de texte
    zone_texte.config(state=tk.DISABLED)


def afficher_corpus(corpus, checkbutton_vars_afficher, checkbutton_vars_comparer, zone_texte):
    selected_source_type = selected_source.get()
    print(selected_source_type)

    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)

    boutons_par_document = {}

    # Débogage
    print("Valeurs de checkbutton_vars_afficher avant la boucle for :", [var.get() for var in checkbutton_vars_afficher])
    print("Valeurs de checkbutton_vars_comparer avant la boucle for :", [var.get() for var in checkbutton_vars_comparer])

    for document in corpus.id2doc.values():
        if selected_source_type == "null" or selected_source_type.lower() in document.url.lower():
            zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", "gras")
            zone_texte.insert(tk.END, f"Auteurs du document : {document.auteur}\n")

            var_afficher = tk.IntVar()
            bouton_check = tk.Checkbutton(zone_texte, text="Afficher", variable=var_afficher, font=("Helvetica", 10),
                                          command=lambda doc=document, var=var_afficher: afficher_details_selectionnes(corpus, checkbutton_vars_afficher, zone_texte))
            bouton_check.document = document
            zone_texte.window_create(tk.END, window=bouton_check)
            zone_texte.insert(tk.END, "\n")

            var_comparer = tk.IntVar()
            bouton_comparer_doc = tk.Checkbutton(
            zone_texte,
            text="Comparer", variable=var_comparer, font=("Helvetica", 10),
            command=lambda doc=document, var=var_comparer: comparer_documents(corpus, checkbutton_vars_comparer, zone_texte))

            bouton_comparer_doc.document = document
            zone_texte.window_create(tk.END, window=bouton_comparer_doc)
            zone_texte.insert(tk.END, "\n")

            boutons_par_document[document] = (var_afficher, var_comparer)

    checkbutton_vars_afficher[:] = [var for var, _ in boutons_par_document.values()]
    checkbutton_vars_comparer[:] = [var_comparer for _, var_comparer in boutons_par_document.values()]

    # Débogage
    print("Valeurs de checkbutton_vars_afficher après la boucle for :", [var.get() for var in checkbutton_vars_afficher])
    print("Valeurs de checkbutton_vars_comparer après la boucle for :", [var.get() for var in checkbutton_vars_comparer])

    zone_texte.config(state=tk.DISABLED)

def comparer_documents(corpus, checkbutton_vars_comparer, zone_texte, numDoc=None):
    documents_selectionnes = [document for document, var in zip(corpus.id2doc.values(), checkbutton_vars_comparer) if var.get()]

    zone_texte.config(state=tk.NORMAL)  # Permet d'éditer la zone de texte

    print("Documents sélectionnés pour comparaison :", documents_selectionnes)  # Débogage

    if len(documents_selectionnes) == 2:
        
        document1 = documents_selectionnes[0]
        document2 = documents_selectionnes[1]
        
        # Vérifier si numDoc est fourni et correspond à l'un des documents sélectionnés
        if numDoc is not None and numDoc not in [document1.numDoc, document2.numDoc]:
            messagebox.showwarning("Erreur", f"L'identifiant unique {numDoc} ne correspond à aucun des documents sélectionnés.")
            zone_texte.config(state=tk.DISABLED)
            return

        # Utiliser la méthode creer_vocabulaire pour obtenir le vocabulaire
        _, _, vocabulaire_corpus, _, _, _ = corpus.creer_vocabulaire()

        # Transformer les documents en vecteurs sur le vocabulaire précédemment construit
        vectorizer = CountVectorizer(vocabulary=vocabulaire_corpus)
        document1_vecteur = vectorizer.transform([document1.texte])
        document2_vecteur = vectorizer.transform([document2.texte])

        # Calculer la similarité entre les deux documents
        similarite = cosine_similarity(document1_vecteur, document2_vecteur).flatten()[0]

        # Récupérer les indices des mots communs
        mots_communs_indices = list(set(document1_vecteur.indices) & set(document2_vecteur.indices))

        # Récupérer les mots communs
        mots_communs = [vocabulaire_corpus[indice] for indice in mots_communs_indices]

        # Calculer le nombre total de mots dans chaque document
        total_mots_document1 = len(document1.texte.split())
        total_mots_document2 = len(document2.texte.split())

        # Afficher la similarité
        zone_texte.config(state=tk.NORMAL)
        zone_texte.delete(1.0, tk.END)
        zone_texte.insert(tk.END, f"Comparaison entre {document1.titre} et {document2.titre}\n\n")
        zone_texte.insert(tk.END, f"Similarité : {similarite}\n\n")
        

        zone_texte.insert(tk.END, f"Informations pour le premier document : \n\n")
        zone_texte.insert(tk.END, f"Titre : {document1.titre}\n")
        zone_texte.insert(tk.END, f"Auteurs : {document1.auteur}\n")
        zone_texte.insert(tk.END, f"URL : {document1.url}\n")
        zone_texte.insert(tk.END, f"Contenu :\n{document1.texte}\n\n")

        zone_texte.insert(tk.END, f"Informations pour le second document :\n\n")
        zone_texte.insert(tk.END, f"Titre : {document2.titre}\n")
        zone_texte.insert(tk.END, f"Auteurs : {document2.auteur}\n")
        zone_texte.insert(tk.END, f"URL : {document2.url}\n")
        zone_texte.insert(tk.END, f"Contenu :\n{document2.texte}\n\n")
        
        if not mots_communs:
            zone_texte.insert(tk.END, "Aucun mot commun trouvé.\n")
        else:
            # Afficher les mots communs dans la zone de texte
            zone_texte.insert(tk.END, "Pourcentage de présence des mots communs :\n\n")
            for mot in mots_communs:
                pour_document1 = document1.texte.lower().count(mot.lower())/total_mots_document1*100
                pour_document2 = document2.texte.lower().count(mot.lower())/total_mots_document1*100
                zone_texte.insert(tk.END, f"- Mot : {mot}\n")
                zone_texte.insert(tk.END, f"{document1.titre} : {pour_document1:.2f} %\n")
                zone_texte.insert(tk.END, f"{document2.titre} : {pour_document2:.2f} %\n\n")
            
        zone_texte.config(state=tk.DISABLED)

    elif len(documents_selectionnes) < 2:
        messagebox.showwarning("Erreur", "Veuillez sélectionner exactement deux documents à comparer.")
    else:
        messagebox.showwarning("Erreur", "Vous avez sélectionné plus de deux documents. Veuillez en choisir seulement deux.")

    zone_texte.config(state=tk.DISABLED)  # Désactive la possibilité d'éditer la zone de texte


''' A UTILISER
def comparer_documents(corpus, checkbutton_vars_comparer, zone_texte):
    documents_selectionnes = [document for document, var in zip(corpus.id2doc.values(), checkbutton_vars_comparer) if var.get()]

    zone_texte.config(state=tk.NORMAL)  # Permet d'éditer la zone de texte

    print("Documents sélectionnés pour comparaison :", documents_selectionnes)  # Débogage

    if len(documents_selectionnes) == 2:
        
        document1 = documents_selectionnes[0]
        document2 = documents_selectionnes[1]
        # Utiliser la méthode creer_vocabulaire pour obtenir le vocabulaire
        _, _, vocabulaire_corpus, _, _, _ = corpus.creer_vocabulaire()

        # Transformer les documents en vecteurs sur le vocabulaire précédemment construit
        vectorizer = CountVectorizer(vocabulary=vocabulaire_corpus)
        document1_vecteur = vectorizer.transform([document1.texte])
        document2_vecteur = vectorizer.transform([document2.texte])

        # Calculer la similarité entre les deux documents
        similarite = cosine_similarity(document1_vecteur, document2_vecteur).flatten()[0]

        # Récupérer les indices des mots communs
        mots_communs_indices = list(set(document1_vecteur.indices) & set(document2_vecteur.indices))

        # Récupérer les mots communs
        mots_communs = [vocabulaire_corpus[indice] for indice in mots_communs_indices]

        # Calculer le nombre total de mots dans chaque document
        total_mots_document1 = len(document1.texte.split())
        total_mots_document2 = len(document2.texte.split())

        # Afficher la similarité
        zone_texte.config(state=tk.NORMAL)
        zone_texte.delete(1.0, tk.END)
        zone_texte.insert(tk.END, f"Comparaison entre {document1.titre} et {document2.titre}\n\n")
        zone_texte.insert(tk.END, f"Similarité : {similarite}\n\n")
        

        zone_texte.insert(tk.END, f"Informations pour le premier document : \n\n")
        zone_texte.insert(tk.END, f"Titre : {document1.titre}\n")
        zone_texte.insert(tk.END, f"Auteurs : {document1.auteur}\n")
        zone_texte.insert(tk.END, f"URL : {document1.url}\n")
        zone_texte.insert(tk.END, f"Contenu :\n{document1.texte}\n\n")

        zone_texte.insert(tk.END, f"Informations pour le second document :\n\n")
        zone_texte.insert(tk.END, f"Titre : {document2.titre}\n")
        zone_texte.insert(tk.END, f"Auteurs : {document2.auteur}\n")
        zone_texte.insert(tk.END, f"URL : {document2.url}\n")
        zone_texte.insert(tk.END, f"Contenu :\n{document2.texte}\n\n")
        
        if not mots_communs:
            zone_texte.insert(tk.END, "Aucun mot commun trouvé.\n")
        else:
            # Afficher les mots communs dans la zone de texte
            zone_texte.insert(tk.END, "Pourcentage de présence des mots communs :\n\n")
            for mot in mots_communs:
                pour_document1 = document1.texte.lower().count(mot.lower())/total_mots_document1*100
                pour_document2 = document2.texte.lower().count(mot.lower())/total_mots_document1*100
                zone_texte.insert(tk.END, f"- Mot : {mot}\n")
                zone_texte.insert(tk.END, f"{document1.titre} : {pour_document1:.2} %\n")
                zone_texte.insert(tk.END, f"{document2.titre} : {pour_document2:.2} %\n\n")
            
        zone_texte.config(state=tk.DISABLED)

    elif len(documents_selectionnes) < 2:
        messagebox.showwarning("Erreur", "Veuillez sélectionner exactement deux documents à comparer.")
    else:
        messagebox.showwarning("Erreur", "Vous avez sélectionné plus de deux documents. Veuillez en choisir seulement deux.")

    zone_texte.config(state=tk.DISABLED)  # Désactive la possibilité d'éditer la zone de texte
'''

'''
def comparer_documents(corpus, checkbutton_vars_comparer, zone_texte):
    documents_selectionnes = [document for document, var in zip(corpus.id2doc.values(), checkbutton_vars_comparer) if var.get()]

    zone_texte.config(state=tk.NORMAL)  # Permet d'éditer la zone de texte

    print("Documents sélectionnés pour comparaison :", documents_selectionnes)  # Débogage

    if len(documents_selectionnes) == 2:
        document1 = documents_selectionnes[0]
        document2 = documents_selectionnes[1]

        # Utiliser la matrice TF-IDF du corpus pour la transformation
        _, _, vocabulaire_corpus, _, _, mat_TFxIDF_corpus = corpus.creer_vocabulaire()

        # Transformer les documents en vecteurs TF-IDF
        vectorizer = TfidfVectorizer(vocabulary=vocabulaire_corpus, use_idf=False)
        
        corpus_texte_nettoye = [corpus.nettoyer_texte(doc.texte) for doc in corpus.id2doc.values()]
        document1_texte_nettoye = corpus.nettoyer_texte(document1.texte)
        document2_texte_nettoye = corpus.nettoyer_texte(document2.texte)
        
        corpus_vecteur = vectorizer.fit_transform(corpus_texte_nettoye)
        document1_vecteur = vectorizer.transform([document1_texte_nettoye])
        document2_vecteur = vectorizer.transform([document2_texte_nettoye])

        # Calculer la similarité entre les deux documents
        similarite = cosine_similarity(document1_vecteur, document2_vecteur).flatten()[0]

        # Récupérer les indices des mots communs
        mots_communs_indices = list(set(document1_vecteur.indices) & set(document2_vecteur.indices))

        # Récupérer les mots communs et leurs valeurs TF-IDF
        mots_communs_info = {mot: {'tfidf': mat_TFxIDF_corpus[:, indice].tolist()} for mot, indice in zip(vocabulaire_corpus, mots_communs_indices)}

        # Afficher les mots communs dans la zone de texte avec leurs valeurs TF-IDF
        zone_texte.insert(tk.END, "Mesure TF-IDF des mots communs :\n\n")
        for mot, info in mots_communs_info.items():
            tfidf_document1 = info['tfidf'][document1.numDoc - 1]
            tfidf_document2 = info['tfidf'][document2.numDoc - 1]

            zone_texte.insert(tk.END, f"- Mot : {mot}\n")
            zone_texte.insert(tk.END, f"{document1.titre} - TF-IDF : {tfidf_document1:.4f}\n")
            zone_texte.insert(tk.END, f"{document2.titre} - TF-IDF : {tfidf_document2:.4f}\n\n")
        

        zone_texte.insert(tk.END, f"Similarité : {similarite}\n\n")

        zone_texte.insert(tk.END, f"Informations pour le premier document : \n\n")
        zone_texte.insert(tk.END, f"Titre : {document1.titre}\n")
        zone_texte.insert(tk.END, f"Auteurs : {document1.auteur}\n")
        zone_texte.insert(tk.END, f"URL : {document1.url}\n")
        zone_texte.insert(tk.END, f"Contenu :\n{document1.texte}\n\n")

        zone_texte.insert(tk.END, f"Informations pour le second document :\n\n")
        zone_texte.insert(tk.END, f"Titre : {document2.titre}\n")
        zone_texte.insert(tk.END, f"Auteurs : {document2.auteur}\n")
        zone_texte.insert(tk.END, f"URL : {document2.url}\n")
        zone_texte.insert(tk.END, f"Contenu :\n{document2.texte}\n\n")

    elif len(documents_selectionnes) < 2:
        messagebox.showwarning("Erreur", "Veuillez sélectionner exactement deux documents à comparer.")
    else:
        messagebox.showwarning("Erreur", "Vous avez sélectionné plus de deux documents. Veuillez en choisir seulement deux.")

    zone_texte.config(state=tk.DISABLED)  # Désactive la possibilité d'éditer la zone de texte
'''

def mesure_corpus(corpus, zone_texte):
    zone_texte.config(state=tk.NORMAL)

    # Utiliser la matrice TF-IDF du corpus pour la transformation
    _, _, vocabulaire_corpus, _, _, mat_TFxIDF_corpus = corpus.creer_vocabulaire()

    # Trier le vocabulaire une fois
    vocabulaire_corpus_trie = sorted(vocabulaire_corpus, key=lambda mot: (not mot.isdigit(), int(mot) if mot.isdigit() else mot.lower()))

    # Transformer les documents en vecteurs TF-IDF (utiliser un sous-ensemble de documents si nécessaire)
    corpus_texte_nettoye = [corpus.nettoyer_texte(doc.texte) for doc in list(corpus.id2doc.values())[:100]]  # Limiter à 100 documents
    vectorizer = TfidfVectorizer(vocabulary=vocabulaire_corpus_trie, use_idf=False)
    corpus_vecteur = vectorizer.fit_transform(corpus_texte_nettoye)

    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)

    # Afficher la mesure TDxIDF pour chaque mot du corpus dans la zone de texte
    zone_texte.insert(tk.END, "Mesure TDxIDF pour chaque mot du corpus :\n\n")
    for mot, indice in zip(vocabulaire_corpus_trie, range(len(vocabulaire_corpus_trie))):
        tfidf_corpus = mat_TFxIDF_corpus[:, indice].tolist()
        
        # Ajouter le mot au texte (en bleu et souligné)
        zone_texte.tag_configure(f"bleu_souligne_{indice}", foreground="blue", underline=True)
        zone_texte.insert(tk.END, f"Mot : {mot}\n", "gras")

        # Ajouter le mot au texte (en lien pour la visualisation)
        zone_texte.tag_configure(f"visualisation_mot_{indice}", foreground="blue", underline=True)
        zone_texte.insert(tk.END, "Visualiser la distribution\n", f"visualisation_mot_{indice}")
        zone_texte.tag_bind(f"visualisation_mot_{indice}", "<Button-1>", lambda event, mot=mot: visualiser_distribution(mot, vocabulaire_corpus_trie, mat_TFxIDF_corpus))

        zone_texte.insert(tk.END, f"Corpus - TDxIDF : {tfidf_corpus}\n\n")

    zone_texte.config(state=tk.DISABLED)

def visualiser_distribution(mot, vocabulaire, mat_TFxIDF):
    # Trouver l'indice du mot dans le vocabulaire
    mot_index = vocabulaire.index(mot)

    # Initialiser la figure pour les graphiques
    plt.figure(figsize=(12, 6))

    tfidf_corpus = mat_TFxIDF[:, mot_index].tolist()

    # Créer un histogramme pour le mot
    plt.hist(np.array(tfidf_corpus), bins=30, edgecolor='black')
    plt.title(f'Distribution TD-IDF pour le mot "{mot}"')
    plt.xlabel('Valeurs TD-IDF')
    plt.ylabel('Fréquence')

    plt.tight_layout()
    plt.show()



'''
def mesure_corpus(corpus, zone_texte):
    zone_texte.config(state=tk.NORMAL)  # Permet d'éditer la zone de texte

    # Utiliser la matrice TF-IDF du corpus pour la transformation
    _, _, vocabulaire_corpus, _, _, mat_TFxIDF_corpus = corpus.creer_vocabulaire()

    # Transformer les documents en vecteurs TF-IDF
    vectorizer = TfidfVectorizer(vocabulary=vocabulaire_corpus, use_idf=False)
    
    corpus_texte_nettoye = [corpus.nettoyer_texte(doc.texte) for doc in corpus.id2doc.values()]
    corpus_vecteur = vectorizer.fit_transform(corpus_texte_nettoye)

    # Afficher la mesure TDxIDF pour chaque mot du corpus dans la zone de texte
    zone_texte.insert(tk.END, "Mesure TDxIDF pour chaque mot du corpus :\n\n")
    for mot, indice in zip(vocabulaire_corpus, range(len(vocabulaire_corpus))):
        tfidf_corpus = mat_TFxIDF_corpus[:, indice].tolist()

        zone_texte.insert(tk.END, f"- Mot : {mot}\n")
        zone_texte.insert(tk.END, f"Corpus - TDxIDF : {tfidf_corpus}\n\n")

    zone_texte.config(state=tk.DISABLED)
'''

'''
def mesure_corpus(corpus, zone_texte):
    zone_texte.config(state=tk.NORMAL)  # Permet d'éditer la zone de texte

    # Utiliser la matrice TF-IDF du corpus pour la transformation
    _, _, vocabulaire_corpus, _, _, mat_TFxIDF_corpus = corpus.creer_vocabulaire()

    # Trier le vocabulaire par ordre alphabétique
    vocabulaire_corpus_trie = sorted(vocabulaire_corpus)

    # Transformer les documents en vecteurs TF-IDF
    vectorizer = TfidfVectorizer(vocabulary=vocabulaire_corpus_trie, use_idf=True)
    
    corpus_texte_nettoye = [corpus.nettoyer_texte(doc.texte) for doc in corpus.id2doc.values()]
    corpus_vecteur = vectorizer.fit_transform(corpus_texte_nettoye)

    # Afficher la mesure TDxIDF pour chaque mot du corpus dans la zone de texte
    zone_texte.insert(tk.END, "Mesure TDxIDF pour chaque mot du corpus :\n\n")
    for mot, indice in zip(vocabulaire_corpus_trie, range(len(vocabulaire_corpus_trie))):
        tfidf_corpus = mat_TFxIDF_corpus[:, indice].tolist()

        zone_texte.insert(tk.END, f"- Mot : {mot}\n")
        zone_texte.insert(tk.END, f"Corpus - TDxIDF : {tfidf_corpus[0]}\n\n")
    
    print("Vocabulaire trié :", vocabulaire_corpus_trie)

    for doc in corpus.id2doc.values():
        print(f"Original: {doc.texte.split()[:10]}")
        print(f"Nettoyé : {corpus.nettoyer_texte(doc.texte).split()[:10]}\n")

    zone_texte.config(state=tk.DISABLED)  # Désactive la possibilité d'éditer la zone de texte
'''
    
'''
def mesure_corpus(corpus, zone_texte):
    zone_texte.config(state=tk.NORMAL)  # Permet d'éditer la zone de texte

    # Utiliser la matrice TF-IDF du corpus pour la transformation
    _, _, vocabulaire_corpus, _, _, mat_TFxIDF_corpus = corpus.creer_vocabulaire()

    # Trier le vocabulaire par ordre alphabétique
    vocabulaire_corpus_trie = sorted(vocabulaire_corpus)

    # Transformer les documents en vecteurs TF-IDF
    vectorizer = TfidfVectorizer(vocabulary=vocabulaire_corpus_trie, use_idf=True)
    
    corpus_texte_nettoye = [corpus.nettoyer_texte(doc.texte) for doc in corpus.id2doc.values()]
    corpus_vecteur = vectorizer.fit_transform(corpus_texte_nettoye)

    # Calculer la moyenne de la mesure TDxIDF pour chaque mot du corpus
    zone_texte.insert(tk.END, "Moyenne de la mesure TDxIDF pour chaque mot du corpus :\n\n")
    for mot, indice_mot in zip(vocabulaire_corpus_trie, range(len(vocabulaire_corpus_trie))):
        zone_texte.insert(tk.END, f"- Mot : {mot}\n")

        # Calculer la moyenne de la mesure TF-IDF pour le mot sur tous les documents
        moyenne_tfidf_corpus = mat_TFxIDF_corpus[:, indice_mot].mean()
            
        zone_texte.insert(tk.END, f"Corpus - Moyenne TDxIDF : {moyenne_tfidf_corpus}\n\n")

    print("Vocabulaire trié :", vocabulaire_corpus_trie)

    for doc in corpus.id2doc.values():
        print(f"Original: {doc.texte.split()[:10]}")
        print(f"Nettoyé : {corpus.nettoyer_texte(doc.texte).split()[:10]}\n")

    zone_texte.config(state=tk.DISABLED)  # Désactive la possibilité d'éditer la zone de texte
'''

def configurer_barre_defilement(event, zone_texte):
    zone_texte.yview_scroll(-1 * (event.delta // 120), "units")

# Créer une nouvelle fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Recherche de documents")

# Créer un cadre pour les libellés "Python"
cadre_python = tk.Frame(fenetre)
cadre_python.pack(side=tk.TOP)

# Ajouter chaque lettre avec sa couleur
label_p = tk.Label(cadre_python, text="P", font=("Helvetica", 30), fg="blue")
label_p.pack(side=tk.LEFT, padx=2)

label_y = tk.Label(cadre_python, text="y", font=("Helvetica", 30), fg="red")
label_y.pack(side=tk.LEFT, padx=2)

label_t = tk.Label(cadre_python, text="t", font=("Helvetica", 30), fg="yellow")
label_t.pack(side=tk.LEFT, padx=2)

label_h = tk.Label(cadre_python, text="h", font=("Helvetica", 30), fg="blue")
label_h.pack(side=tk.LEFT, padx=2)

label_o = tk.Label(cadre_python, text="o", font=("Helvetica", 30), fg="green")
label_o.pack(side=tk.LEFT, padx=2)

label_n = tk.Label(cadre_python, text="n", font=("Helvetica", 30), fg="red")
label_n.pack(side=tk.LEFT, padx=2)

# Créer un champ de texte (Entry) pour les mots-clés
entry_mots_clefs = Entry(fenetre, width=40)
entry_mots_clefs.pack(pady=10)

#Créer un cadre pour les boutons
cadre_boutons = tk.Frame(fenetre)
cadre_boutons.pack()

# Créer un bouton pour effectuer la recherche
bouton_recherche = Button(cadre_boutons, text="Rechercher", command=lambda: effectuer_recherche(entry_mots_clefs, corpus, variables, zone_texte, selected_source, checkbutton_vars_afficher, checkbutton_vars_comparer))
bouton_recherche.pack(side=tk.LEFT, padx=5)

# Créer un bouton pour afficher tout le corpus
bouton_afficher_corpus = Button(cadre_boutons, text="Afficher Tout le Corpus", command=lambda: afficher_corpus(corpus, checkbutton_vars_afficher, checkbutton_vars_comparer, zone_texte))
bouton_afficher_corpus.pack(side=tk.LEFT, padx=5)

bouton_mesure = Button(cadre_boutons, text="Mesure du corpus", command=lambda: mesure_corpus(corpus, zone_texte))
bouton_mesure.pack(side=tk.LEFT, padx=5)

#Espace pour sélectionner un type de source
# Sources disponibles
source = ["Reddit", "ArXiv"]
selected_source = tk.StringVar()

# Variables pour stocker l'état des Checkbuttons
variables = [tk.IntVar() for _ in source]

# Créer les Radiobuttons et les ajouter à la fenêtre
for i, option in enumerate(source):
    radiobutton = tk.Radiobutton(cadre_boutons, text=option, variable=selected_source, value=option)
    radiobutton.pack(side=tk.LEFT, padx=5)

# Créer un cadre (Frame) pour contenir la zone de texte et la barre de défilement
cadre_texte = tk.Frame(fenetre)
cadre_texte.pack(expand=True, fill='both')

# Créer un widget de texte pour afficher le contenu dans le cadre
zone_texte = Text(cadre_texte, wrap=tk.WORD, width=80, height=20)
zone_texte.pack(side=tk.LEFT, expand=True, fill='both')

# Créer une barre de défilement sur le côté du cadre
barre_defilement = Scrollbar(cadre_texte, command=zone_texte.yview)
barre_defilement.pack(side=tk.RIGHT, fill=tk.Y)

# Configurer la zone de texte pour utiliser la barre de défilement
zone_texte.config(yscrollcommand=barre_defilement.set)

# Configurer la barre de défilement pour répondre à la molette de la souris
zone_texte.bind("<MouseWheel>", lambda event: configurer_barre_defilement(event, zone_texte))

# Configurer le style de texte pour la couleur rouge
zone_texte.tag_configure("rouge", foreground="red")

# Créer un style de texte pour le texte en gras
zone_texte.tag_configure("gras", font=("Helvetica", 10, "bold"))



# Démarrer la boucle principale Tkinter
fenetre.mainloop()
