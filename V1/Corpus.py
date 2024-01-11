# Correction de G. Poux-Médard, 2021-2022
#from DesignPattern import *
from Classes import Author
from Classes_filles import RedditDocument, ArxivDocument
 
import re
import pandas as pd
from scipy.sparse import csr_matrix 
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer

# =============== 2.7 : CLASSE CORPUS ===============
#@singleton
class Corpus:
    #Constucteur, intialisation des attributs
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    #Fonction pour ajouter un document au corpus
    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

# =============== 2.8 : REPRESENTATION ===============
    # Fonction pour afficher les documents du corpus
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]
    #td5
        #for doc in docs:
        #    print(f"Source: {doc.getType()} - {doc.__str__()}")
        '''
        for doc in docs:
            if isinstance(doc, RedditDocument):
                    print(f"Source: {doc.getType()} - {doc.__str__()}")
            elif isinstance(doc, ArxivDocument):
                    print(f"Source: {doc.getType()} - {doc.__str__()}")
        '''
        #de base dans la correction
        print("\n".join(list(map(repr, docs))))

    # Fonction pour obtenir une représentation de l'objet
    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))
        
        return "\n".join(list(map(str, docs)))
   