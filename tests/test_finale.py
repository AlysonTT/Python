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

# Variables pour stocker l'état des Checkbuttons "Afficher"
checkbutton_vars_afficher = {}

# Variables pour stocker l'état des Checkbuttons "Comparer"
checkbutton_vars_comparer = {}


def effectuer_recherche(entry_mots_clefs, corpus, zone_texte, selected_source, checkbutton_vars_afficher, checkbutton_vars_comparer):
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
    
    # Afficher les trois meilleurs résultats (avec score non nul)
    if not documents_retrouves:
        zone_texte.insert(tk.END, "Aucun résultat trouvé dans le corpus.")
    else:
        for i, (document, score_document) in enumerate(documents_retrouves):
            if (score_document != 0 or i < 3):
                zone_texte.insert(tk.END, f"Résultat {i + 1} :\n", "gras")
                zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", )
                zone_texte.insert(tk.END, f"Auteurs du document : {document.auteur}\n")
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

                zone_texte.insert(tk.END, "=" * 150 + "\n")
            

                boutons_par_document[document] = (var_afficher, var_comparer)

    checkbutton_vars_afficher.update({doc.numDoc: var_afficher for doc, (var_afficher, _) in boutons_par_document.items()})
    checkbutton_vars_comparer.update({doc.numDoc: var_comparer for doc, (_, var_comparer) in boutons_par_document.items()})

    # Désactiver la modification de la zone de texte
    zone_texte.config(state=tk.DISABLED)


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
        zone_texte.insert(tk.END, f"URL du document : {document.url}\n")
        zone_texte.insert(tk.END, f"Contenu du document :\n{document.texte}\n")
        zone_texte.insert(tk.END, "=" * 150 + "\n")

    # Désactiver la modification de la zone de texte
    zone_texte.config(state=tk.DISABLED)

def afficher_corpus(corpus, checkbutton_vars_afficher, checkbutton_vars_comparer, zone_texte):
    selected_source_type = selected_source.get()

    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)

    boutons_par_document = {}

    # Débogage
    print("Valeurs de checkbutton_vars_afficher avant la boucle for :", [var.get() for var in checkbutton_vars_afficher.values()])
    print("Valeurs de checkbutton_vars_comparer avant la boucle for :", [var.get() for var in checkbutton_vars_comparer.values()])

    for document in corpus.id2doc.values():
        if selected_source_type == "null" or selected_source_type.lower() in document.url.lower():
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

    checkbutton_vars_afficher.update({doc.numDoc: var_afficher for doc, (var_afficher, _) in boutons_par_document.items()})
    checkbutton_vars_comparer.update({doc.numDoc: var_comparer for doc, (_, var_comparer) in boutons_par_document.items()})

    # Débogage
    print("Valeurs de checkbutton_vars_afficher après la boucle for :", [var.get() for var in checkbutton_vars_afficher.values()])
    print("Valeurs de checkbutton_vars_comparer après la boucle for :", [var.get() for var in checkbutton_vars_comparer.values()])

    zone_texte.config(state=tk.DISABLED)

def comparer_documents(corpus, checkbutton_vars_comparer, zone_texte, numDoc):
    # Récupérer le document par son identifiant unique
    document = next(doc for doc in corpus.id2doc.values() if doc.numDoc == numDoc)

    # Récupérer les documents sélectionnés en utilisant l'identifiant unique
    numeros_selectionnes = [doc for doc, var in checkbutton_vars_comparer.items() if var.get()]

    zone_texte.config(state=tk.NORMAL)  # Permet d'éditer la zone de texte

    print("Documents sélectionnés pour comparaison :", numeros_selectionnes)  # Débogage
    print("longueur :" ,len(numeros_selectionnes))
    if len(numeros_selectionnes) == 2:
        num_doc1 = numeros_selectionnes[0]
        num_doc2 = numeros_selectionnes[1]

        # Récupérer les documents correspondants aux numéros
        document1 = next(doc for doc in corpus.id2doc.values() if doc.numDoc == num_doc1)
        document2 = next(doc for doc in corpus.id2doc.values() if doc.numDoc == num_doc2)

        # Comparaison simple des textes des deux documents
        zone_texte.delete(1.0, tk.END)
        zone_texte.insert(tk.END, f"Comparaison entre {document1.titre} et {document2.titre}\n\n")
        zone_texte.insert(tk.END, "Titre du document 1:\n")
        zone_texte.insert(tk.END, document1.titre)
        zone_texte.insert(tk.END, "\n\nTitre du document 2:\n")
        zone_texte.insert(tk.END, document2.titre)

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
bouton_recherche = Button(cadre_boutons, text="Rechercher", command=lambda: clear_tous_les_boutons(checkbutton_vars_afficher, checkbutton_vars_comparer) or effectuer_recherche(entry_mots_clefs, corpus, zone_texte, selected_source, checkbutton_vars_afficher, checkbutton_vars_comparer))
bouton_recherche.pack(side=tk.LEFT, padx=5)

# Créer un bouton pour afficher tout le corpus
#appel à lear fct
bouton_afficher_corpus = Button(cadre_boutons, text="Afficher Tout le Corpus", command=lambda: clear_tous_les_boutons(checkbutton_vars_afficher, checkbutton_vars_comparer) or afficher_corpus(corpus, checkbutton_vars_afficher, checkbutton_vars_comparer, zone_texte))
bouton_afficher_corpus.pack(side=tk.LEFT, padx=5)

# Ajoutez cette ligne dans la création du cadre_boutons
bouton_clear = Button(cadre_boutons, text="Clear", command=lambda: clear_tous_les_boutons(checkbutton_vars_afficher, checkbutton_vars_comparer))
bouton_clear.pack(side=tk.LEFT, padx=5)


#Espace pour sélectionner un type de source
# Sources disponibles
source = ["Reddit", "ArXiv"]
selected_source = tk.StringVar()


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
