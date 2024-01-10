import tkinter as tk
from tkinter import messagebox
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import numpy as np

from Deselection import Deselection
deselection = Deselection()

class Affichage:
    def __init__(self):
        # Initialiser ici les éléments communs à toutes les fonctions d'affichage
        pass

    '''
    Affiche les détails des documents sélectionnés dans la zone de texte.

    Paramètres : 
        - corpus : L'objet corpus contenant les documents.
        - zone_texte : Le widget de zone de texte dans lequel afficher les détails.
        - numDoc : Le numéro du document à afficher. Attribut de la classe Document.
        - vars_afficher : Un dictionnaire de variables associées aux boutons "Afficher" pour chaque document.

    Algorithme :
        Récupère le document associé au numDoc dans l'objet corpus.
        Active la modification de la zone de texte.
        Efface le contenu précédent de la zone de texte.
        Récupère les documents sélectionnés en fonction des variables associées aux boutons "Afficher".
        Affiche les détails des documents sélectionnés : le titre, l'auteur, la date, l'URL et le contenu du document.
    '''
    def afficher_details_selectionnes(self, corpus, zone_texte, numDoc, vars_afficher):
        document = next(doc for doc in corpus.id2doc.values() if doc.numDoc == numDoc)

        zone_texte.config(state=tk.NORMAL)
        zone_texte.delete(1.0, tk.END)

        # Récupérer les documents sélectionnés
        documents_selectionnes = [doc for doc, var in zip(corpus.id2doc.values(), vars_afficher.values()) if var.get()]

        # Afficher les détails des documents sélectionnés
        for document in documents_selectionnes:
            zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", "gras")
            zone_texte.insert(tk.END, f"Auteur du document : {document.auteur}\n")
            zone_texte.insert(tk.END, f"Date du document : {document.date}\n")
            zone_texte.insert(tk.END, f"Lien du document : {document.url}\n")
            zone_texte.insert(tk.END, f"Contenu du document :\n{document.texte}\n")
            zone_texte.insert(tk.END, "=" * 150 + "\n")

        # Désactiver la modification de la zone de texte
        zone_texte.config(state=tk.DISABLED)
        
    '''Affichage du Corpus dans son intégralité'''
    def afficher_corpus(self, corpus, zone_texte, checkbutton, vars_afficher, vars_comparer):
        # Etape 1 : Effacer le contenu précédent du widget de texte
        zone_texte.config(state=tk.NORMAL)
        zone_texte.delete(1.0, tk.END) 
        
        #deselectionne le check du type si active
        checkbutton.deselect()

        '''AJOUTER'''
        boutons_par_document = {}

        # Débogage
        print("Valeurs de checkbutton_vars_afficher avant la boucle for :", [var.get() for var in vars_afficher.values()])
        print("Valeurs de checkbutton_vars_comparer avant la boucle for :", [var.get() for var in vars_comparer.values()])

        '''AJOUTER'''

        # Etape 2 : Afficher l'ensemble du corpus    
        for document in corpus.id2doc.values():
            ''''AJOUTER'''
            zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", "gras")
            zone_texte.insert(tk.END, f"Auteurs du document : {document.auteur}\n")

            var_afficher = tk.IntVar()
            bouton_check = tk.Checkbutton(
                zone_texte, text="Afficher", variable=var_afficher, font=("Helvetica", 10),
                command=lambda doc=document, var=var_afficher: self.afficher_details_selectionnes(corpus, zone_texte, doc.numDoc, vars_afficher))
            bouton_check.document = document
            zone_texte.window_create(tk.END, window=bouton_check)
            zone_texte.insert(tk.END, "\n")

            var_comparer = tk.IntVar()
            bouton_comparer_doc = tk.Checkbutton(
                    zone_texte,
                    text="Comparer", variable=var_comparer, font=("Helvetica", 10),
                    command=lambda doc=document: self.comparer_documents(corpus, zone_texte, vars_afficher, vars_comparer, doc.numDoc))

            bouton_comparer_doc.document = document
            zone_texte.window_create(tk.END, window=bouton_comparer_doc)
            zone_texte.insert(tk.END, "\n")

            boutons_par_document[document] = (var_afficher, var_comparer)
            '''AJOUTER'''

        '''AJOUTER'''
        vars_afficher.update({doc.numDoc: var_afficher for doc, (var_afficher, _) in boutons_par_document.items()})
        vars_comparer.update({doc.numDoc: var_comparer for doc, (_, var_comparer) in boutons_par_document.items()})
        vars_afficher.update({doc.numDoc: var_afficher for doc, (var_afficher, _) in boutons_par_document.items()})
        vars_comparer.update({doc.numDoc: var_comparer for doc, (_, var_comparer) in boutons_par_document.items()})
        '''AJOUTER'''

        # Activer la modification de la zone de texte
        zone_texte.config(state=tk.DISABLED)

    '''Visualiser la distribution'''
    def visualiser_distribution(self, mot, vocabulaire, mat_TFxIDF):
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
    Comparer deux documents sélectionnés dans le corpus en utilisant la similarité cosinus et affiche les détails de la comparaison.
   
    Paramètres : 
        - corpus: L'objet corpus contenant les documents.
        - zone_texte: La zone de texte où afficher les résultats.
        - vars_afficher : un dictionnaire de variables associées aux boutons "Afficher" pour chaque document.
        - vars_comparer: Dictionnaire de variables associées aux boutons “Comparer” pour chaque document.
        - numDoc: L'identifiant unique du document sur lequel l'utilisateur a cliqué pour lancer la comparaison.
    
    Algorithme :
        Récupère les documents sélectionnés en utilisant les identifiants uniques.
        Initialise les variables pour les deux documents à comparer.
        Utilise la méthode creer_vocabulaire de la classe Corpus pour obtenir le vocabulaire du corpus.
        Transforme les documents en vecteurs sur le vocabulaire précédemment construit à l'aide de la similarité cosinus
        Calcule la similarité entre les deux documents.
        Récupère les indices des mots communs et les mots communs eux-mêmes.
        Calcule le pourcentage de présence des mots communs dans chaque document.
        Affiche la similarité et les informations détaillées pour chaque document.
        Réinitialise tous les boutons de comparaison dans les variables associées.
        Affiche un message d'erreur si le nombre de documents sélectionnés n'est pas exactement deux.
        Désactive la modification de la zone de texte.           
    '''
    def comparer_documents(self, corpus, zone_texte, vars_afficher, vars_comparer, numDoc):
        # Récupérer les documents sélectionnés en utilisant l'identifiant unique
        numeros_selectionnes = [doc for doc, var in vars_comparer.items() if var.get()]

        zone_texte.config(state=tk.NORMAL)  # Permet d'éditer la zone de texte

        print("Documents sélectionnés pour comparaison :", numeros_selectionnes)  # Débogage
        print("longueur :" ,len(numeros_selectionnes))
        print("longeur check ", len(vars_comparer))
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
            zone_texte.insert(tk.END, f"Date du document : {document1.date}\n")
            zone_texte.insert(tk.END, f"URL : {document1.url}\n")
            zone_texte.insert(tk.END, f"Contenu :\n{document1.texte}\n\n")

            zone_texte.insert(tk.END, f"Informations pour le second document :\n\n")
            zone_texte.insert(tk.END, f"Titre : {document2.titre}\n")
            zone_texte.insert(tk.END, f"Auteurs : {document2.auteur}\n")
            zone_texte.insert(tk.END, f"Date du document : {document2.date}\n")
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
            
            deselection.clear_tous_les_boutons(vars_afficher, vars_comparer)
            # Réinitialiser les variables de comparaison
            vars_comparer = {}
            
            zone_texte.config(state=tk.DISABLED)

        elif len(numeros_selectionnes) < 2:
            messagebox.showwarning("Erreur", "Veuillez sélectionner exactement deux documents à comparer.")
        else:
            messagebox.showwarning("Erreur", "Vous avez sélectionné plus de deux documents. Veuillez en choisir seulement deux.")

        zone_texte.config(state=tk.DISABLED)  # Désactive la possibilité d'éditer la zone de texte