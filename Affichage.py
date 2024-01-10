import tkinter as tk
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import numpy as np

from Fonctions_interface import comparer_documents
class Affichage:
    def __init__(self):
        # Initialiser ici les éléments communs à toutes les fonctions d'affichage
        pass

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
                    command=lambda doc=document: comparer_documents(corpus, zone_texte, vars_afficher, vars_comparer, doc.numDoc))

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
        
    def mesure_corpus(self, corpus, zone_texte):
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
            zone_texte.tag_bind(f"visualisation_mot_{indice}", "<Button-1>", lambda event, mot=mot: self.visualiser_distribution(mot, vocabulaire_corpus_trie, mat_TFxIDF_corpus))

            zone_texte.insert(tk.END, f"Corpus - TDxIDF : {tfidf_corpus}\n\n")

        zone_texte.config(state=tk.DISABLED)
