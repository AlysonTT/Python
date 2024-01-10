'''Section 1: Importation des bibliothèques'''
import tkinter as tk
from tkinter import Text, Scrollbar, Entry, Button, Label
import pickle

# Vérification de l'importation du module Corpus
try:
    from Corpus import Corpus
except ImportError:
    print("Échec de l'importation du module Corpus.")

'''Section 2: Chargement du corpus'''
# Charge le corpus depuis le fichier
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

'''Section 3: Initialisation'''
# Liste des auteurs utilisés pour le afficher dans la fenetre
liste_auteurs = set()

# Variables pour stocker l'état des Checkbuttons "Afficher"
checkbutton_vars_afficher = {}

# Variables pour stocker l'état des Checkbuttons "Comparer"
checkbutton_vars_comparer = {}

# Ajoute chaque auteur à l'ensemble (en traitant les clés avec plusieurs noms)
for auteur, index in corpus.aut2id.items():
    # Vérifie si la clé contient plusieurs noms
    if ',' in auteur:
        noms_separes = [nom.strip() for nom in auteur.split(',')]
        liste_auteurs.update(noms_separes)
    else:
        liste_auteurs.add(auteur)

# Converti l'ensemble en une liste triée
liste_auteurs = sorted(list(liste_auteurs))

'''Section 4 : Configurer la barre de defilement'''
def configurer_barre_defilement(event):
    zone_texte.yview_scroll(-1 * (event.delta // 120), "units")

'''Section 5 : importation des classes pour utiliser leurs fonctions par la suite'''
from Affichage import Affichage
affichage = Affichage()
from Selection import Selection
selection = Selection()
from Deselection import Deselection
deselection = Deselection()
from RechercheAnalyse import RechercheAnalyse
rechercheAnalyse = RechercheAnalyse()

'''Section 6 : Création de la fenêtre avec ses différents éléments'''

# Crée une nouvelle fenêtre Tkinter
fenetre = tk.Tk()

# Largeur et hauteur de l'écran
largeur_ecran = fenetre.winfo_screenwidth()
hauteur_ecran = fenetre.winfo_screenheight()

# Position pour que le centre de la fenêtre soit aligné avec le centre de l'écran
x_position = (largeur_ecran - fenetre.winfo_reqwidth()) // 2  - 550
y_position = (hauteur_ecran - fenetre.winfo_reqheight()) // 2 - 250

# Position initiale de la fenêtre
fenetre.geometry(f"+{x_position}+{y_position}")

# Titre de la fenetre
fenetre.title("Moteur de recherche d'information")

# Cadre pour les libellés "Python"
cadre_python = tk.Frame(fenetre)
cadre_python.pack(side=tk.TOP)

# Ajoute chaque lettre cote à cote pour Python avec sa couleur 
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

# Etiquette pour explication des mots à l'utilisateur
label_mots_cles = Label(fenetre, text="Veuillez entrer un ou des mots-clés séparés par un espace :")
label_mots_cles.pack(pady=5)

# Cadre pour organiser les éléments principale
cadre_principal = tk.Frame(fenetre)
cadre_principal.pack(pady=10)

# Champ de texte pour les mots-clés
entry_mots_clefs = Entry(cadre_principal, width=40)
entry_mots_clefs.grid(row=0, column=0, padx=5)

# Bouton pour effectuer la recherche
bouton_recherche = Button(cadre_principal, text="Rechercher", command=lambda: rechercheAnalyse.effectuer_recherche(corpus, zone_texte, entry_mots_clefs, entry_date, source, variables, listebox_auteurs, checkbutton_vars_afficher, checkbutton_vars_comparer))
bouton_recherche.grid(row=0, column=1, padx=5)

# Cadre pour les boutons et les options
cadre_boutons_options = tk.Frame(fenetre)
cadre_boutons_options.pack()

# Espace pour sélectionner un type de source
cadre_sources = tk.Frame(cadre_boutons_options)
cadre_sources.grid(row=0, column=0, padx=5, pady=5)

# Etiquette Source
label_source = tk.Label(cadre_sources, text="Sources :")
label_source.grid(row=0, column=0, pady=5)

# Sources disponibles
source = ["Reddit", "ArXiv"]

# Variables pour stocker l'état des Checkbuttons
variables = [tk.IntVar() for _ in source]

# Crée les Checkbuttons et les ajoute au sous-cadre cadre_sources
for i, option in enumerate(source):
    checkbutton = tk.Checkbutton(cadre_sources, text=option, variable=variables[i], command=lambda i=i: selection.selection_unique(i, variables))
    checkbutton.grid(row=1, column=i, padx=5, pady=5)

# Espace pour sélectionner un ou plusieurs auteurs
cadre_auteurs = tk.Frame(cadre_boutons_options)
cadre_auteurs.grid(row=0, column=1, padx=5, pady=5)

# Etiquette Auteur
label_auteurs = tk.Label(cadre_auteurs, text="Auteurs :")
label_auteurs.grid(row=0, column=1, pady=5)

# Listebox pour afficher la liste des auteurs
listebox_auteurs = tk.Listbox(cadre_auteurs, selectmode=tk.MULTIPLE, height=5, width=30)
for auteur in liste_auteurs:
    listebox_auteurs.insert(tk.END, auteur)
listebox_auteurs.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")
    
# Checkbutton pour désélectionner tous les auteurs
checkbutton_deselection = tk.Checkbutton(cadre_auteurs, text="Désélectionner tous les auteurs", command=lambda: deselection.deselectionner_tous_les_auteurs(listebox_auteurs, checkbutton_deselection))
checkbutton_deselection.grid(row=2, column=1, pady=5)

# Barre de défilement pour la Listebox des auteurs
scrollbar_auteurs = tk.Scrollbar(cadre_auteurs, orient=tk.VERTICAL, command=listebox_auteurs.yview)
scrollbar_auteurs.grid(row=1, column=2, sticky="ns", pady=10)

# Associe la barre de défilement à la Listebox des auteurs
listebox_auteurs.config(yscrollcommand=scrollbar_auteurs.set)

#Espace pour ecrire une date
cadre_date = tk.Frame(cadre_boutons_options)
cadre_date.grid(row=0, column=2, padx=5, pady=5)

# Etiquette pour la date
label_date = Label(cadre_date, text="Veuillez entrer la date (AAAA/MM/JJ) :")
label_date.grid(row=0, column=2, pady=5)

# Champ de texte pour la date
entry_date = Entry(cadre_date, width=20)
entry_date.grid(row=1, column=2, pady=5)

# Bouton pour afficher tout le corpus
bouton_afficher_corpus = Button(cadre_boutons_options, text="Afficher tout le corpus", command=lambda: affichage.afficher_corpus(corpus, zone_texte, checkbutton, checkbutton_vars_afficher, checkbutton_vars_comparer))
bouton_afficher_corpus.grid(row=0, column=4, padx=5)

# Checkbutton pour supprimer la sélection des documents à comparer
bouton_clear = tk.Checkbutton(cadre_boutons_options, text="Supprimer la sélection des documents à comparer", command=lambda: deselection.clear_tous_les_boutons(checkbutton_vars_afficher, checkbutton_vars_comparer))
bouton_clear.grid(row=0, column=3, padx=5)

# Bouton pour la matrice TFxIDF
bouton_mesure = Button(cadre_boutons_options, text="Matrice TFxIDF du vocabulaire du corpus", command=lambda: rechercheAnalyse.mesure_corpus(corpus, zone_texte))
bouton_mesure.grid(row=0, column=5, padx=5)

# Cdre pour contenir la zone de texte et la barre de défilement
cadre_texte = tk.Frame(fenetre)
cadre_texte.pack(expand=True, fill='both')

# Widget de texte pour afficher le contenu dans le cadre
zone_texte = Text(cadre_texte, wrap=tk.WORD, width=80, height=15)
zone_texte.pack(side=tk.LEFT, expand=True, fill='both')

# Barre de défilement sur le côté du cadre
barre_defilement = Scrollbar(cadre_texte, command=zone_texte.yview)
barre_defilement.pack(side=tk.RIGHT, fill=tk.Y)

# Configure la zone de texte pour utiliser la barre de défilement
zone_texte.config(yscrollcommand=barre_defilement.set)

# etiquette pour la frise temporelle
label_temporel = Label(fenetre, text="Veuillez entrer le mot-clé pour obtenir sa frise temporelle :")
label_temporel.pack(pady=5)

#Cadre pour les boutons
cadre_temporel = tk.Frame(fenetre)
cadre_temporel.pack(pady=10)

# Champ de texte pour le mot ou on souhaite connaitre sa frise temporelle
entry_temporel = Entry(cadre_temporel, width=40)
entry_temporel.grid(row=0, column=0, padx=5)

# Bouton pour effectuer la recherche
bouton_temporel = Button(cadre_temporel, text="Générer Frise Temporelle", command=lambda:rechercheAnalyse.generer_frise_temporelle(corpus, entry_temporel))
bouton_temporel.grid(row=0, column=1, padx=5)

# Configure la barre de défilement pour répondre à la molette de la souris
zone_texte.bind("<MouseWheel>", configurer_barre_defilement)

# Style de texte pour la couleur rouge
zone_texte.tag_configure("rouge", foreground="red")

# Style de texte pour la couleur bleu
zone_texte.tag_configure("bleu", foreground="blue")

# Style de texte pour la couleur vert
zone_texte.tag_configure("vert", foreground="green")

# Style de texte pour le texte en gras
zone_texte.tag_configure("gras", font=("Helvetica", 10, "bold"))

# Démarre la boucle principale Tkinter
fenetre.mainloop()