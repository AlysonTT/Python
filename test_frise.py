import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button
import pickle

# Vérification de l'importation du module Corpus
try:
    from Corpus import Corpus
except ImportError:
    print("Échec de l'importation du module Corpus.")

# Fonction pour traiter la date et générer la frise temporelle
def generer_frise_temporelle():
    mot_recherche = entry_mot.get()

    # Demander à l'utilisateur de choisir le fichier .pkl
    fichier_corpus = "corpus.pkl"

    if fichier_corpus:
        # Charger les données depuis le fichier .pkl
        with open(fichier_corpus, "rb") as f:
            corpus_objet = pickle.load(f)

        # Vérifier si l'objet chargé est un DataFrame ou un Corpus
        if isinstance(corpus_objet, Corpus):
            # Ajoutez le code nécessaire pour travailler avec l'objet Corpus
            print("Objet Corpus chargé avec succès!")
            # Ajoutez ici le code pour manipuler l'objet Corpus selon vos besoins
            informations_temporelles = corpus_objet.extraire_informations_temporelles(mot_recherche)
            
            # Vérifier si les informations sont dans le format attendu
            if informations_temporelles:
                plt.figure(figsize=(10, 6))
                # Graphique avec une ligne continue
                plt.plot(list(informations_temporelles.keys()), list(informations_temporelles.values()), label=f'Évolution de "{mot_recherche}" dans le temps', linestyle='-')
                    
                # Choisissez un nombre fixe d'axes des x
                num_axes_x = 6
                num_points = len(informations_temporelles)
                step = max(1, num_points // num_axes_x)

                # Définir les étiquettes de l'axe x
                x_labels = list(informations_temporelles.keys())[::step]
                plt.xticks(x_labels)

                plt.xlabel('Période')
                plt.ylabel('Fréquence du Mot')
                plt.title(f'Évolution temporelle du mot "{mot_recherche}" dans le corpus')

                plt.show()
            else:
                print("Impossible d'extraire les informations temporelles du Corpus.")  
        else:
            print("L'objet chargé n'est pas un objet Corpus.")

# Interface utilisateur avec Tkinter
fenetre = Tk()
fenetre.title("Analyse Temporelle de Mots")

# Éléments d'interface
Label(fenetre, text="Mot à rechercher :").pack(pady=10)
entry_mot = Entry(fenetre)
entry_mot.pack(pady=10)
Button(fenetre, text="Générer Frise Temporelle", command=generer_frise_temporelle).pack(pady=10)

# Lancement de la boucle principale
fenetre.mainloop()
