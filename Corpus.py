# Correction de G. Poux-Médard, 2021-2022

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

    # =============== TD6 2.1 : Nettoyage du texte ===============
    def nettoyer_texte(self, texte):
        # Mise en minuscules
        texte = texte.lower()

        # Remplacement des passages à la ligne
        texte = texte.replace("\n", " ")

        # Remplacement des ponctuations et des chiffres
        texte = re.sub(r'[^\w\s]', '', texte)

        return texte
    
    # =============== TD 6 2.4 : Création du Vocabulaire et du tableau de fréquence ===============
    # =============== TD 7 1.1 : Création du dictionnaire vocab avec tri alphabétique ===============
    # =============== TD 7 1.2 : Création de la matrice creuse ===============
    # =============== TD 7 1.3 : Création de dictionnaire vocab_mat_TF avec remplissage grace a mat_TF ===============
    # =============== TD 7 1.4 : Création d'une 2eme matrice creuse, mesure TFxIDF===============

    def creer_vocabulaire(self):
        nombre_doc_total = len(self.id2doc)
        #utiliser pour créer le tableau de fréquence
        vocabulaire = set()
        occurrences = {}
        mot_id = 0
        # pour chaque mot, une liste des doc où on le trouve
        mot_par_doc = {}
        #utiliser pour créer le dictionnaire des mots
        vocab = {}
        #utiliser pour la matrice creuse math_TF
        row, col, data = [], [], []
        #utiliser pour créer le dictionnaire des mots avec mat_TF pour le remplir
        vocab_mat_TF = {}

        
        # Parcourir tous les documents du corpus
        for doc in self.id2doc.values():
            #nettoyage du texte avant de chercher les futurs mots du vocabulaire
            texte_nettoye = self.nettoyer_texte(doc.texte)

            # On divise le texte en mots en utilisant différents délimiteurs 
            # on ajoute dans "mots" les mots trouves dans le doc
            mots = [mot for mot in re.split(r'\s+|[.,;\'"!?()]', texte_nettoye) if mot]
            # Ajouter chaque mot unique au vocabulaire
            vocabulaire.update(mots)

            for mot in mots:
                #Cree une liste du nouveau trouve à mot_par_doc
                if mot not in mot_par_doc:
                    mot_par_doc[mot] = set()
                    #a chaque fois qu'on trouve un mot qui est pas dans le doc
                    #on incremente l'id du mot
                    mot_id+=1
                mot_par_doc[mot].add(doc.numDoc)

                # Ajout au mot son identifiant unique
                vocab.setdefault(mot, mot_id)

                # Compter les occurrences de chaque mot
                occurrences[mot] = occurrences.get(mot, 0) + 1
                
                # Ajout au doc une occurence du mot trouvé dans celui-ci
                row.append(doc.numDoc)
                col.append(vocab[mot])
                data.append(1)  # a chaque occurrence on ajoute 1


        # Construire un tableau de fréquences avec la bibliothèque Pandas
        freq = pd.DataFrame(list(occurrences.items()), columns=['Mot', 'Occurences'])
        
        #ajout d'une nouvelle colonne dans le tableau des fréquences
        #qui indique dans combien de doc le mot est présent
        freq['Nombre de document'] = [len(docs) for docs in mot_par_doc.values()]

        # Tri par ordre décroissant des occurrences
        freq = freq.sort_values(by='Occurences', ascending=False)

        #On trie le dictionnaire dans l'ordre alphabetique des mots
        vocab = {mot: {'id': vocab[mot], 'occurrences': occurrences[mot], 'nb_doc': len(mot_par_doc[mot])} for mot, vocab[mot] in sorted(vocab.items())}  

        #ajouter 1 au nombre des colonnes(mot) et de ligne(nb_doc) pour avoir accès aux mots du dernier doc
        mat_TF= csr_matrix((data, (row, col)), shape=(nombre_doc_total+1, len(vocabulaire)+1)).toarray()        

        # Utilisation de la bibliothèque scikit-learn pour calculer le score TF-IDF
        tfidf_transformer = TfidfTransformer()
        mat_TFxIDF = tfidf_transformer.fit_transform(mat_TF).toarray()
        
        # On compte le nombre d'éléments non nuls sur chaque colonne
        # pour avoir le nombre de doc qui contient le mot
        #axis=0 colonne et axis=1 ligne
        nombre_doc_contenant_mot = np.count_nonzero(mat_TF, axis=0)

        # On fait la somme des valeurs de chaque colonne pour avoir le nombre d'occurence de chaque mot
        somme_colonnes = np.sum(mat_TF, axis=0)

        vocab_mat_TF = {mot: {'id': info['id'], 'occurrences': somme_colonnes[info['id']], 'nb_doc': nombre_doc_contenant_mot[info['id']]} for mot, info in sorted(vocab.items())}

        return vocab, vocab_mat_TF, list(vocabulaire), freq, mat_TF, mat_TFxIDF
    
     #Fonction pour avoir les informations temporelle d'un mot
    def extraire_informations_temporelles(self, mot_recherche):
        informations_temporelles = {}

        for doc_info in self.id2doc.values():
            contenu = doc_info.texte  # Récupérer le texte
            date = doc_info.date  # Récupérer la date

            # Vérifier si le mot recherché est présent dans le contenu du document
            for mot in contenu.split():
                if mot in mot_recherche:
                    # Ajouter les informations à la période correspondante
                    if date not in informations_temporelles:
                        informations_temporelles[date] = 0
                    informations_temporelles[date] += 1

        return informations_temporelles