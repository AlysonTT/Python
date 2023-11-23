# Correction de G. Poux-Médard, 2021-2022

from Classes import Author
from Classes_filles import RedditDocument, ArxivDocument
 
import re
import pandas as pd

# =============== 2.7 : CLASSE CORPUS ===============
#@singleton
class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

# =============== 2.8 : REPRESENTATION ===============
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

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))
        
        return "\n".join(list(map(str, docs)))


    # =============== TD6 1.1 : Recherche mot-clé ===============
    def search(self, texte, mot_cle):
        res = []
        #insensible à la case et trouve le mot en entier
        matches = re.finditer(r'\b{}\b'.format(re.escape(mot_cle)), texte, flags=re.IGNORECASE)
        passages = [match.group(0) for match in matches]
        if passages:
            res.append({'passages': passages})
        return res

    # =============== TD6 1.2 : Construction du concordancier ===============
    def concorde(self, texte, mot_cle, contexte=10):
        res = []

        matches = re.finditer(r'\b{}\b'.format(re.escape(mot_cle)), texte, flags=re.IGNORECASE)
            
        for match in matches:
            start = max(0, match.start() - contexte)
            end = min(len(texte), match.end() + contexte)
            context = texte[start:end]

            res.append({
                'contexte_gauche': context[:contexte],
                'motif_trouve': match.group(0),
                'contexte_droit': context[-contexte:]
            })

        # Convertir les résultats en un DataFrame pandas
        df = pd.DataFrame(res)
        return df

    # =============== TD 6 2.3 : Création du Vocabulaire et du tableau de fréquence ===============
    # =========== TD7 1.1
    # ============= TD7 voir pour trier les mots

    def creer_vocabulaire(self):
        vocabulaire = set()
        occurrences = {}
        # pour chaque mot, une liste des doc où on le trouve
        mot_par_doc = {}
        # initialisation 
        vocab = {}
        mot_id = 0

        # Parcourir tous les documents du corpus
        for doc in self.id2doc.values():
            # On divise le texte en mots en utilisant différents délimiteurs 
            # on ajoute dans "mots" les mots trouves dans le doc
            mots = [mot for mot in re.split(r'\s+|[.,;\'"!?()]', doc.texte) if mot]
            # Ajouter chaque mot unique au vocabulaire
            vocabulaire.update(mots)
            
            ### 2.2 Création de la matrice
            from scipy.sparse import csr_matrix 
            import numpy as np
            #créeation de la matrice
            #pas le bonne matrice utiliser csr_matrix
            #pas compris
            #mat_TF = np.zeros((len(self.id2doc.values()),len(vocabulaire)))
            #print(mat_TF)

            for mot in mots:
                # Ajouter l'identifiant du document à mot_par_doc
                if mot not in mot_par_doc:
                    mot_par_doc[mot] = set()
                    #a chaque fois qu'on trouve un mot qui est pas dans le doc
                    #on incremente l'id du mot
                    mot_id+=1
                mot_par_doc[mot].add(doc.numDoc)

                #ajoute au mot son identifiant unique
                vocab.setdefault(mot, mot_id)

                # Compter les occurrences de chaque mot
                occurrences[mot] = occurrences.get(mot, 0) + 1

                #ICI AJOUTER LES VALEURS DANS MAT_TF
                #Peut-etre pas en faite
            

        # Construire un tableau de fréquences avec la bibliothèque Pandas
        freq = pd.DataFrame(list(occurrences.items()), columns=['Mot', 'Occurences'])
        
        #ajout d'une nouvelle colonne dans le tableau des fréquences
        #qui indique dans combien de doc le mot est présent
        freq['Nombre de document'] = [len(docs) for docs in mot_par_doc.values()]

        # Tri par ordre décroissant des occurrences
        freq = freq.sort_values(by='Occurences', ascending=False)

        #Test definitir nb doc
        #nb_doc=[len(docs) for docs in mot_par_doc.values()

        #trie le dictionnaire dans l'ordre alphabetique des mots
        vocab = {mot: {'id': info, 'occurrences': occurrences[mot], 'nb doc': len(mot_par_doc[mot])} for mot, info in sorted(vocab.items())}  

        #créeation de la matrice
        #mat_TF = csr_matrix(freq)
        #mat_TF = csr_matrix((4, 4), dtype = np.int8).toarray() #fonctionne
        '''
        row = np.array([0, 1, 3, 0])
        col = np.array([0, 2, 1, 2])
        data = np.array([3, 1, 8, 9])
        mat_TF = csr_matrix((data, (row, col)), shape=(4, 4)).toarray()
        '''
        #docs est associé au doc_1, doc_2, ..., doc_n
        #regarder pour chaque documents si le mots est dans le document et creer une liste
        mat_TF = csr_matrix( ( ) , shape=(len(docs), len(vocabulaire))).toarray()

        return vocab, list(vocabulaire), freq, mat_TF

        #return list(vocabulaire), freq

    # 1.2


    ################### TD7
    '''
    from collections import defaultdict

    def construire_vocab(docs):
        vocab = {}
        mot_id = 0

        # Parcourir tous les documents
        for doc in docs:
            # Découper le document en mots et les convertir en minuscules
            mots = [mot.lower() for mot in doc.split()]

            # Supprimer les doublons
            mots_uniques = list(set(mots))

            # Trier les mots par ordre alphabétique
            mots_uniques.sort()

            # Mettre à jour le dictionnaire vocab
            for mot in mots_uniques:
                if mot not in vocab:
                    # Si le mot n'est pas déjà dans le dictionnaire, l'ajouter
                    vocab[mot] = {'id': mot_id, 'occurrences': mots.count(mot)}
                    mot_id += 1
                else:
                    # Si le mot est déjà dans le dictionnaire, mettre à jour le nombre d'occurrences
                    vocab[mot]['occurrences'] += mots.count(mot)

        return vocab

    # Exemple d'utilisation avec une liste de documents
    documents = ["Ceci est un exemple de document.", "Un autre exemple de document."]
    resultat_vocab = construire_vocab(documents)

    # Afficher le résultat
    for mot, info in resultat_vocab.items():
        print(f"Mot: {mot}, ID: {info['id']}, Occurrences: {info['occurrences']}")
    '''