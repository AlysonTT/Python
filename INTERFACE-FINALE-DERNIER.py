
'''Section 1: Importation des bibliothèques'''

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

'''Section 2: Chargement du corpus'''

# Charger le corpus depuis le fichier
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

'''Section 3: Initialisation'''

# Liste des auteurs utilisés pour le afficher dans la fenetre
liste_auteurs = set()

# Variables pour stocker l'état des Checkbuttons "Afficher"
checkbutton_vars_afficher = {}

# Variables pour stocker l'état des Checkbuttons "Comparer"
checkbutton_vars_comparer = {}

# Ajouter chaque auteur à l'ensemble (en traitant les clés avec plusieurs noms)
for auteur, index in corpus.aut2id.items():
    # Vérifier si la clé contient plusieurs noms
    if ',' in auteur:
        noms_separes = [nom.strip() for nom in auteur.split(',')]
        liste_auteurs.update(noms_separes)
    else:
        liste_auteurs.add(auteur)

# Convertir l'ensemble en une liste triée
liste_auteurs = sorted(list(liste_auteurs))

'''Section 4 : Fonctions Utilitaires'''

'''Cette section regroupe plusieurs fonctions utilitaires 
qui facilitent la gestion des sélections d'utilisateurs, 
la validation des dates et des auteurs, etc.'''

#fonction qui permet d'avoir qu'un type de source selectionné
def selection_unique(index):
    for i, var in enumerate(variables):
        if i != index:
            var.set(0)

#fonction pour savoir quel type est sélectionné
def checkbutton_selection():
    # Afficher les éléments sélectionnés
    options_selectionnees = [source[i] for i, var in enumerate(variables) if var.get()]
    if options_selectionnees:
        return ", ".join(options_selectionnees)
    else:
        return "null"

#fonction pour savoir quels auteurs ont été sélectionné
def auteurs_selection():
    auteurs_selectionnes = [listebox_auteurs.get(i) for i in listebox_auteurs.curselection()]
    if auteurs_selectionnes:
        return ", ".join(auteurs_selectionnes)
    else:
        return "null"

#fonction pour deselectionner tous les auteurs quand on appuie sur un checkbutton
def deselectionner_tous_les_auteurs():
    # Désélectionne tous les éléments de la listebox
    listebox_auteurs.selection_clear(0, tk.END)
    # On met l'état du checkbutton en non coché
    checkbutton_deselection.deselect()
    
    
#fonction pour vérifier qu'une date est valide
def est_date_valide(annee, mois, jour):
    # Vérification de l'année (entre 1900 et 2024)
    if not (1900 <= annee <= 2024):
        return False

    # Vérification du mois
    if not (1 <= mois <= 12):
        return False

    # Vérification du jour en fonction du mois
    jours_dans_le_mois = {
        1: 31, 2: 29 if (annee % 4 == 0 and annee % 100 != 0) or (annee % 400 == 0) else 28,
        3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    if not (1 <= jour <= jours_dans_le_mois[mois]):
        return False

    return True

'''Section 5: Fonction de recherche '''

#fonction pour effectuer une recherche avec des mots-clés
#un type de source ou des auteurs spécifiés ou non  
def effectuer_recherche():
    # Etape 1 : obtenir les différents éléments de recherche sélectionné par l'utilisateur à partir des différents éléments
    #mots-cles entrez dans le champ texte
    mots_clefs = entry_mots_clefs.get().split()
    
    #date entrez dans le champ texte
    date_entre = entry_date.get().strip()

    # Vérifier qu'il y a un seul mot
    date_lenght = date_entre.split()
    if len(date_lenght) == 1:
            #verifie le format
            date_regex = re.compile(r'^(\d{4})/(\d{2})/(\d{2})$')
            date =date_regex.match(date_entre)
            if date:
                annee, mois, jour = map(int, date.groups())

                 # Vérifier la validité de la date
                if not est_date_valide(annee, mois, jour):
                    messagebox.showerror("Erreur", "Veuillez entrer une date valide.")
            else:
                messagebox.showerror("Erreur", "Veuillez entrer une date dans le format AAAA/MM/JJ.")
    elif len(date_lenght)>2:
        # Afficher un message d'erreur si la date n'est pas dans le bon format
        messagebox.showerror("Erreur", "Veuillez entrer une date.")

    #Recuperer le type de source selectionne
    type = checkbutton_selection()

    #Recuperer les auteurs selectionnes
    auteurs = auteurs_selection() 

    #liste des auteurs selectionne avec un autre format
    liste_auteurs_choisi = auteurs.split(',')

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
        #any pour au moins un des mots clé all pour tous

        type_auteur = False
        #lise des auteurs du document
        liste_auteurs_doc = document.auteur.split(',')
        
        # Supprimer les espaces avant et après chaque nom dans les deux listes
        liste_auteurs_choisi = [auteur.strip() for auteur in liste_auteurs_choisi]
        liste_auteurs_doc = [auteur.strip() for auteur in liste_auteurs_doc]

        #on regarde si un des auteurs a écrit le document
        for auteur in liste_auteurs_doc:
            if auteur in liste_auteurs_choisi:
                type_auteur = True
                break
        
        if auteurs == "null":
            type_auteur = True

        # On cherche les mots clés dans le texte ou dans le titre du document
        if mots_trouves_texte or mots_trouves_titre:           
            if document not in documents_retrouves:
                if type_auteur==True and (type == "null" or type.lower() in document.url.lower()) and (document.date == date_entre or len(date_entre)==0):
                    documents_retrouves.append((document, score_document))

    # Trier les résultats par score de similarité
    documents_retrouves.sort(key=lambda x: x[1], reverse=True)

    # Effacer le contenu précédent du widget de texte
    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)

    '''AJOUTER'''
    boutons_par_document = {}
    '''AJOUTER'''

    # Afficher les trois meilleurs résultats (avec score non nul)
    if not documents_retrouves:
        zone_texte.insert(tk.END, "Aucun résultat trouvé dans le corpus.")
    else:
        meilleur_resultat_affiche = 0
        for i, (document, score_document) in enumerate(documents_retrouves):
            #if score_document != 0 and meilleur_resultat_affiche < 3:
            #if meilleur_resultat_affiche < 3:
            if (score_document != 0 or meilleur_resultat_affiche < 3) and (mots_trouves_titre or meilleur_resultat_affiche < 3):

                zone_texte.insert(tk.END, f"Résultat {i + 1} :\n", "gras")
                zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n")
                zone_texte.insert(tk.END, f"Auteurs du document: {''.join(document.auteur)}\n")
                zone_texte.insert(tk.END, f"Date du document : {document.date}\n")
                zone_texte.insert(tk.END, f"Lien du document : {document.url}\n")

                if document.texte  != "":
                    #si le doc est vide ne pas écrire
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
                
                # Mettre en bleu les auteurs selectionnés
                for auteur in liste_auteurs_choisi:
                    start_index = "1.0"
                    while start_index:
                        start_index = zone_texte.search(auteur, start_index, tk.END, nocase=True)
                        if start_index:
                            end_index = f"{start_index}+{len(auteur)}c"
                            zone_texte.tag_add("bleu", start_index, end_index)
                            start_index = end_index

                # Mettre en vert la date écrite
                if len(date_entre)!=0:
                    start_index = "1.0"
                    while start_index:
                        start_index = zone_texte.search(date_entre, start_index, tk.END, nocase=True)
                        if start_index:
                            end_index = f"{start_index}+{len(date_entre)}c"
                            zone_texte.tag_add("vert", start_index, end_index)
                            start_index = end_index

                zone_texte.insert(tk.END, f"Score de similarité: {score_document}\n")
                
                '''AJOUTER'''
                var_afficher = tk.IntVar()
                bouton_check = tk.Checkbutton(
                    zone_texte, text="Afficher", variable=var_afficher, font=("Helvetica", 10),
                    command=lambda doc=document, var=var_afficher: afficher_details_selectionnes(corpus, checkbutton_vars_afficher, zone_texte, doc.numDoc))
                bouton_check.document = document
                zone_texte.window_create(tk.END, window=bouton_check)
                zone_texte.insert(tk.END, "\n")
                

                var_comparer = tk.IntVar()
                bouton_comparer_doc = tk.Checkbutton(
                    zone_texte,
                    text="Comparer", variable=var_comparer, font=("Helvetica", 10),
                    command=lambda doc=document, var=var_comparer: comparer_documents(corpus, checkbutton_vars_comparer, zone_texte, doc.numDoc))
                bouton_comparer_doc.document = document
                zone_texte.window_create(tk.END, window=bouton_comparer_doc)
                zone_texte.insert(tk.END, "\n")
                '''AJOUTER'''
                
                zone_texte.insert(tk.END, "=" * 150 + "\n")
                meilleur_resultat_affiche += 1
            #else:zone_texte.insert(tk.END, "Aucun résultat trouvé dans le corpus.")

                '''AJOUTER'''
                boutons_par_document[document] = (var_afficher, var_comparer)
                '''AJOUTER'''
        '''AJOUTER'''
        checkbutton_vars_afficher.update({doc.numDoc: var_afficher for doc, (var_afficher, _) in boutons_par_document.items()})
        checkbutton_vars_comparer.update({doc.numDoc: var_comparer for doc, (_, var_comparer) in boutons_par_document.items()})
        '''AJOUTER'''

        # Désactiver la modification de la zone de texte
        zone_texte.config(state=tk.DISABLED)

'''AJOUTER'''

'''Section 6 : Affichage des Détails des Documents Sélectionnés'''

def afficher_details_selectionnes(corpus, checkbutton_vars_afficher, zone_texte, numDoc):
    document = next(doc for doc in corpus.id2doc.values() if doc.numDoc == numDoc)

    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)

    # Récupérer les documents sélectionnés
    documents_selectionnes = [document for document, var in zip(corpus.id2doc.values(), checkbutton_vars_afficher.values()) if var.get()]

    # Afficher les détails des documents sélectionnés
    for document in documents_selectionnes:
        zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", "gras")
        zone_texte.insert(tk.END, f"Auteur du document : {document.auteur}\n")
        zone_texte.insert(tk.END, f"Date du document : {document.date}\n")
        zone_texte.insert(tk.END, f"URL du document : {document.url}\n")
        zone_texte.insert(tk.END, f"Contenu du document :\n{document.texte}\n")
        zone_texte.insert(tk.END, "=" * 150 + "\n")

    # Désactiver la modification de la zone de texte
    zone_texte.config(state=tk.DISABLED)
'''AJOUTER'''

'''Section 7 : Affichage du Corpus dans son intégralité'''

def afficher_corpus():
    # Etape 1 : Effacer le contenu précédent du widget de texte
    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END) 
    
    #deselectionne le check du type si active
    checkbutton.deselect()

    
    '''AJOUTER'''
    
    boutons_par_document = {}

    # Débogage
    print("Valeurs de checkbutton_vars_afficher avant la boucle for :", [var.get() for var in checkbutton_vars_afficher.values()])
    print("Valeurs de checkbutton_vars_comparer avant la boucle for :", [var.get() for var in checkbutton_vars_comparer.values()])

    '''AJOUTER'''

    # Etape 2 : Afficher l'ensemble du corpus    
    for document in corpus.id2doc.values():
        ''''AJOUTER'''

        zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", "gras")
        zone_texte.insert(tk.END, f"Auteurs du document : {document.auteur}\n")

        var_afficher = tk.IntVar()
        bouton_check = tk.Checkbutton(
            zone_texte, text="Afficher", variable=var_afficher, font=("Helvetica", 10),
            command=lambda doc=document, var=var_afficher: afficher_details_selectionnes(corpus, checkbutton_vars_afficher, zone_texte, doc.numDoc))
        bouton_check.document = document
        zone_texte.window_create(tk.END, window=bouton_check)
        zone_texte.insert(tk.END, "\n")

        var_comparer = tk.IntVar()
        bouton_comparer_doc = tk.Checkbutton(
                zone_texte,
                text="Comparer", variable=var_comparer, font=("Helvetica", 10),
                command=lambda doc=document, var=var_comparer: comparer_documents(corpus, checkbutton_vars_comparer, zone_texte, doc.numDoc))

        bouton_comparer_doc.document = document
        zone_texte.window_create(tk.END, window=bouton_comparer_doc)
        zone_texte.insert(tk.END, "\n")

        boutons_par_document[document] = (var_afficher, var_comparer)
        '''AJOUTER'''

        # Affiche les informations de chaque document
        zone_texte.insert(tk.END, f"Titre du document: {document.titre}\n")
        zone_texte.insert(tk.END, f"Auteurs du document: {''.join(document.auteur)}\n")
        zone_texte.insert(tk.END, f"Date du document : {document.date}\n")
        zone_texte.insert(tk.END, f"Type du document: {document.url}\n")
        if document.texte  != "":
            #si le doc est vide ne pas écrire
            zone_texte.insert(tk.END, f"Contenu du document :\n{document.texte}\n")
        zone_texte.insert(tk.END, "=" * 150 + "\n")
    
    '''AJOUTER'''
    checkbutton_vars_afficher.update({doc.numDoc: var_afficher for doc, (var_afficher, _) in boutons_par_document.items()})
    checkbutton_vars_comparer.update({doc.numDoc: var_comparer for doc, (_, var_comparer) in boutons_par_document.items()})
    checkbutton_vars_afficher.update({doc.numDoc: var_afficher for doc, (var_afficher, _) in boutons_par_document.items()})
    checkbutton_vars_comparer.update({doc.numDoc: var_comparer for doc, (_, var_comparer) in boutons_par_document.items()})
    '''AJOUTER'''

    # Activer la modification de la zone de texte
    zone_texte.config(state=tk.DISABLED)
    
def comparer_documents(corpus, checkbutton_vars_comparer, zone_texte, numDoc):
    

    # Récupérer les documents sélectionnés en utilisant l'identifiant unique
    numeros_selectionnes = [doc for doc, var in checkbutton_vars_comparer.items() if var.get()]

    zone_texte.config(state=tk.NORMAL)  # Permet d'éditer la zone de texte

    print("Documents sélectionnés pour comparaison :", numeros_selectionnes)  # Débogage
    print("longueur :" ,len(numeros_selectionnes))
    print("longeur check ", len(checkbutton_vars_comparer))
    if len(numeros_selectionnes) == 2:
        num_doc1 = numeros_selectionnes[0]
        num_doc2 = numeros_selectionnes[1]

        # Récupérer les documents correspondants aux numéros
        document1 = next(doc for doc in corpus.id2doc.values() if doc.numDoc == num_doc1)
        document2 = next(doc for doc in corpus.id2doc.values() if doc.numDoc == num_doc2)


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
                pour_document2 = document2.texte.lower().count(mot.lower())/total_mots_document2*100
                zone_texte.insert(tk.END, f"- Mot : {mot}\n")
                zone_texte.insert(tk.END, f"{document1.titre} : {pour_document1:.2f} %\n")
                zone_texte.insert(tk.END, f"{document2.titre} : {pour_document2:.2f} %\n\n")
        
        clear_tous_les_boutons(checkbutton_vars_afficher, checkbutton_vars_comparer)
        # Réinitialiser les variables de comparaison
        checkbutton_vars_comparer = {}
        
        zone_texte.config(state=tk.DISABLED)

    elif len(numeros_selectionnes) < 2:
        messagebox.showwarning("Erreur", "Veuillez sélectionner exactement deux documents à comparer.")
    else:
        messagebox.showwarning("Erreur", "Vous avez sélectionné plus de deux documents. Veuillez en choisir seulement deux.")

    zone_texte.config(state=tk.DISABLED)  # Désactive la possibilité d'éditer la zone de texte


def clear_tous_les_boutons(checkbutton_vars_afficher, checkbutton_vars_comparer):
    for var_afficher in checkbutton_vars_afficher.values():
        var_afficher.set(0)

    for var_comparer in checkbutton_vars_comparer.values():
        var_comparer.set(0)




def configurer_barre_defilement(event):
    zone_texte.yview_scroll(-1 * (event.delta // 120), "units")

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


def generer_frise_temporelle():
    mot_recherche = entry_mot_temporel.get()

    # Vérifier qu'il y a un seul mot
    mots = mot_recherche.strip().split()
    if len(mots) == 1:
        # On va recuperer les donnees temporelle du mot entrez par l'utilisateur
        informations_temporelles = corpus.extraire_informations_temporelles(mot_recherche)
            
        if informations_temporelles:
            plt.figure(figsize=(10, 6))

            # Tri des clés dans l'ordre chronologique
            sorted_keys = sorted(informations_temporelles.keys())
            sorted_values = [informations_temporelles[key] for key in sorted_keys]

            # Graphique avec une ligne continue
            plt.plot(sorted_keys, sorted_values, label=f'Évolution de "{mot_recherche}" dans le temps', linestyle='-')
                    
            # Choisissez un nombre fixe d'axes des x
            num_axes_x = 6
            num_points = len(informations_temporelles)
            step = max(1, num_points // num_axes_x)

            # Définir les étiquettes de l'axe x
            x_labels = sorted_keys[::step]
            plt.xticks(x_labels)

            plt.xlabel('Période')
            plt.ylabel('Fréquence du Mot')
            plt.title(f'Évolution temporelle du mot "{mot_recherche}" dans le corpus')

            plt.show()

    else:
        messagebox.showerror("Erreur", "Veuillez entrer un seul mot.")



# Créer une nouvelle fenêtre Tkinter
fenetre = tk.Tk()
# Obtenez la largeur et la hauteur de l'écran
largeur_ecran = fenetre.winfo_screenwidth()
hauteur_ecran = fenetre.winfo_screenheight()

# Définissez la position initiale de la fenêtre (x_position, y_position)
fenetre.geometry(f"+{largeur_ecran // 4}+0")

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

# Ajouter une étiquette
label_mots_cles = Label(fenetre, text="Veuillez entrer des mots-clés séparés par un espace :")
label_mots_cles.pack(pady=5)

# Créer un champ de texte (Entry) pour les mots-clés
entry_mots_clefs = Entry(fenetre, width=40)
entry_mots_clefs.pack(pady=10)

#Créer un cadre pour les boutons et des options
cadre_boutons_options = tk.Frame(fenetre)
cadre_boutons_options.pack()

# Espace pour sélectionner un type de source
cadre_sources = tk.Frame(cadre_boutons_options)
cadre_sources.grid(row=0, column=0, padx=5, pady=5)

label_source = tk.Label(cadre_sources, text="Sources :")
label_source.grid(row=0, column=0, pady=5)

# Sources disponibles
source = ["Reddit", "ArXiv"]

# Variables pour stocker l'état des Checkbuttons
variables = [tk.IntVar() for _ in source]

# Créer les Checkbuttons et les ajouter au sous-cadre
for i, option in enumerate(source):
    checkbutton = tk.Checkbutton(cadre_sources, text=option, variable=variables[i], command=lambda i=i: selection_unique(i))
    checkbutton.grid(row=1, column=i, padx=5, pady=5)

# Espace pour sélectionner un ou plusieurs auteurs
cadre_auteurs = tk.Frame(cadre_boutons_options)
cadre_auteurs.grid(row=0, column=1, padx=5, pady=5)

label_auteurs = tk.Label(cadre_auteurs, text="Auteurs :")
label_auteurs.grid(row=0, column=1, pady=5)

# Listebox pour afficher la liste des auteurs
listebox_auteurs = tk.Listbox(cadre_auteurs, selectmode=tk.MULTIPLE, height=5, width=30)
for auteur in liste_auteurs:
    listebox_auteurs.insert(tk.END, auteur)
listebox_auteurs.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")
    
# Checkbutton pour désélectionner tous les auteurs
checkbutton_deselection = tk.Checkbutton(cadre_auteurs, text="Désélectionner tous les auteurs", command=deselectionner_tous_les_auteurs)
checkbutton_deselection.grid(row=2, column=1, pady=5)

# Barre de défilement pour la Listebox
scrollbar_auteurs = tk.Scrollbar(cadre_auteurs, orient=tk.VERTICAL, command=listebox_auteurs.yview)
scrollbar_auteurs.grid(row=1, column=2, sticky="ns", pady=10)

# Associer la barre de défilement à la Listebox
listebox_auteurs.config(yscrollcommand=scrollbar_auteurs.set)

#Espace pour ecrire une date
cadre_date = tk.Frame(cadre_boutons_options)
cadre_date.grid(row=0, column=2, padx=5, pady=5)

# Ajouter une étiquette
label_date = Label(cadre_date, text="Veuillez entrer la date (AAAA/MM/JJ) :")
label_date.grid(row=0, column=2, pady=5)

# Créer un champ de texte pour la date
entry_date = Entry(cadre_date, width=20)
entry_date.grid(row=1, column=2, pady=5)

# Créer un bouton pour effectuer la recherche
bouton_recherche = Button(cadre_boutons_options, text="Rechercher", command=effectuer_recherche)
bouton_recherche.grid(row=0, column=3, padx=5)

# Créer un bouton pour afficher tout le corpus
bouton_afficher_corpus = Button(cadre_boutons_options, text="Afficher Tout le Corpus", command=afficher_corpus)
bouton_afficher_corpus.grid(row=0, column=4, padx=5)

# Ajoutez cette ligne dans la création du cadre_boutons
bouton_clear = Button(cadre_boutons_options, text="Clear", command=lambda: clear_tous_les_boutons(checkbutton_vars_afficher, checkbutton_vars_comparer))
bouton_clear.grid(row=1, column=2, padx=5)

bouton_mesure = Button(cadre_boutons_options, text="Mesure du corpus", command=lambda: mesure_corpus(corpus, zone_texte))
bouton_mesure.grid(row=1, column=3, padx=5)


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

#Espace pour la frise temporelle
# Ajouter une étiquette
label_temporel = Label(fenetre, text="Veuillez entrer le mot-clé pour obtenir sa frise temporelle :")
label_temporel.pack(pady=5)

# Créer un champ de texte pour le mot ou on veut avoir sa frise temporelle
entry_mot_temporel = Entry(fenetre, width=40)
entry_mot_temporel.pack(pady=10)

#Créer un cadre pour les boutons
cadre_temporel = tk.Frame(fenetre)
cadre_temporel.pack()

# Créer un bouton pour effectuer la recherche
bouton_temporel = Button(cadre_temporel, text="Générer Frise Temporelle", command=generer_frise_temporelle)
bouton_temporel.pack(side=tk.LEFT, padx=5)

# Configurer la barre de défilement pour répondre à la molette de la souris
zone_texte.bind("<MouseWheel>", configurer_barre_defilement)

# Configurer le style de texte pour la couleur rouge
zone_texte.tag_configure("rouge", foreground="red")

# Configurer le style de texte pour la couleur bleu
zone_texte.tag_configure("bleu", foreground="blue")

# Configurer le style de texte pour la couleur vert
zone_texte.tag_configure("vert", foreground="green")

# Créer un style de texte pour le texte en gras
zone_texte.tag_configure("gras", font=("Helvetica", 10, "bold"))

# Démarrer la boucle principale Tkinter
fenetre.mainloop()