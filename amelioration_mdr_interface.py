import tkinter as tk
from tkinter import Text, Scrollbar, Entry, Button, Label
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Vérification de l'importation du module Corpus
try:
    from Corpus import Corpus
except ImportError:
    print("Échec de l'importation du module Corpus.")

# Charger le corpus depuis le fichier
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

# Liste des auteurs utilisés pour le afficher dans la fenetre
liste_auteurs = []
# Ajouter chaque auteur à la liste (en traitant les clés avec plusieurs noms)
for auteur, index in corpus.aut2id.items():
    # Vérifier si la clé contient plusieurs noms
    if ',' in auteur:
        noms_separes = [nom.strip() for nom in auteur.split(',')]
        liste_auteurs.extend(noms_separes)
    else:
        liste_auteurs.append(auteur)

#fonction qui permet d'avoir qu'un type de source selectionné
def selection_unique(index):
    for i, var in enumerate(variables):
        if i != index:
            var.set(0)

#fonction pour savoir quel type est sélectionné
def checkbutton_selection():
    # Afficher l'élément sélectionné
    options_selectionnees = [source[i] for i, var in enumerate(variables) if var.get()]
    if options_selectionnees:
        return ", ".join(options_selectionnees)
    else:
        return "null"

#fonction pour savoir quel auteurs ont été sélectionné
def auteurs_selection():
    auteurs_selectionnes = [listebox_auteurs.get(i) for i in listebox_auteurs.curselection()]
    if auteurs_selectionnes:
        return ", ".join(auteurs_selectionnes)
    else:
        return "null"

#fonction pour effectuer une recherche avec des mots-clés
#un type de source ou des auteurs spécifiés ou non
def effectuer_recherche():
    #Recuperer le type de source selectionne
    type = checkbutton_selection()

    #Recuperer les auteurs selectionnes
    auteurs = auteurs_selection()    

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

    #liste des auteurs selectionne
    liste_auteurs_choisi = auteurs.split(',')

    # Afficher les documents qui contiennent au moins un mot-clé avec le score de similarité
    documents_retrouves = []
    for document, score_document in zip(corpus.id2doc.values(), similarite):
        mots_trouves_texte = any(mot.lower() in document.texte.lower() for mot in mots_clefs)
        mots_trouves_titre = any(mot.lower() in document.titre.lower() for mot in mots_clefs)

        type_auteur = False
        #lise des auteurs du document
        liste_auteurs_doc = document.auteur.split(',')

        #on regarde si un des auteurs a écrit le document
        for auteur in liste_auteurs_choisi:
            if auteur in liste_auteurs_doc:
                type_auteur = True
                break
        
        if auteurs == "null":
            type_auteur = True
        
        # On cherche les mots clés dans le texte ou dans le titre du document
        if mots_trouves_texte or mots_trouves_titre:           
            if document not in documents_retrouves:
                if type_auteur==True and type == "null" or type.lower() in document.url.lower():
                    documents_retrouves.append((document, score_document))
                

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
            if meilleur_resultat_affiche < 3:
                zone_texte.insert(tk.END, f"Résultat {i + 1} :\n", "gras")
                zone_texte.insert(tk.END, f"Titre du document: {document.titre}\n")
                zone_texte.insert(tk.END, f"Auteurs du document: {document.auteur}\n")
                zone_texte.insert(tk.END, f"Type du document: {document.url}\n")
                zone_texte.insert(tk.END, f"Contenu du document:\n{document.texte}\n")
                    
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
            #else:zone_texte.insert(tk.END, "Aucun résultat trouvé dans le corpus.")
    
        # Désactiver la modification de la zone de texte
        zone_texte.config(state=tk.DISABLED)


def afficher_corpus():
    #Recuperer le type de source
    type = checkbutton_selection()

    #Recuperer les auteurs
    auteurs = auteurs_selection()

    # Effacer le contenu précédent du widget de texte
    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)

    #liste des auteurs selectionne
    liste_auteurs_choisi = auteurs.split(',')

    # Afficher l'ensemble du corpus    
    for document in corpus.id2doc.values():
        type_auteur = False
        #lise des auteurs du document
        liste_auteurs_doc = document.auteur.split(',')

        #on regarde si un des auteurs a écrit le document
        for auteur in liste_auteurs_choisi:
            if auteur in liste_auteurs_doc:
                type_auteur = True
                break

        # Vérifiez également la condition de type
        type_condition = type == "null" or type.lower() in document.url.lower()

        #si aucun auteurs selectionné, on affiche tous les documents
        if auteurs == "null":
            type_auteur = True

        # Vérifiez si la condition est satisfaite
        if type_auteur and type_condition:
            zone_texte.insert(tk.END, f"Titre du document: {document.titre}\n")
            zone_texte.insert(tk.END, f"Auteurs du document: {''.join(document.auteur)}\n")
            zone_texte.insert(tk.END, f"Type du document: {document.url}\n")
            zone_texte.insert(tk.END, f"Contenu du document:\n{document.texte}\n")
            zone_texte.insert(tk.END, "=" * 150 + "\n")

    # Activer la modification de la zone de texte
    zone_texte.config(state=tk.DISABLED)

def configurer_barre_defilement(event):
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
bouton_recherche = Button(cadre_boutons, text="Rechercher", command=effectuer_recherche)
bouton_recherche.pack(side=tk.LEFT, padx=5)

# Créer un bouton pour afficher tout le corpus
bouton_afficher_corpus = Button(cadre_boutons, text="Afficher Tout le Corpus", command=afficher_corpus)
bouton_afficher_corpus.pack(side=tk.LEFT, padx=5)

#Espace pour sélectionner un type de source
# Sources disponibles
source = ["Reddit", "ArXiv"]

# Variables pour stocker l'état des Checkbuttons
variables = [tk.IntVar() for _ in source]

# Créer les Checkbuttons et les ajouter à la fenêtre
for i, option in enumerate(source):
    checkbutton = tk.Checkbutton(cadre_boutons, text=option, variable=variables[i], command=lambda i=i: selection_unique(i))
    checkbutton.pack(side=tk.LEFT, padx=5)

#Espace pour sélectionner un ou plusieurs auteurs

# Listebox pour afficher la liste des auteurs
listebox_auteurs = tk.Listbox(cadre_boutons, selectmode=tk.MULTIPLE, height=5, width=30)
for auteur in liste_auteurs:
    listebox_auteurs.insert(tk.END, auteur)
listebox_auteurs.pack(side=tk.LEFT, padx=5, pady=10)

# Barre de défilement pour la Listebox
scrollbar_auteurs = tk.Scrollbar(cadre_boutons, orient=tk.VERTICAL, command=listebox_auteurs.yview)
scrollbar_auteurs.pack(side=tk.RIGHT, fill=tk.Y)

# Associer la barre de défilement à la Listebox
listebox_auteurs.config(yscrollcommand=scrollbar_auteurs.set)

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
zone_texte.bind("<MouseWheel>", configurer_barre_defilement)

# Configurer le style de texte pour la couleur rouge
zone_texte.tag_configure("rouge", foreground="red")

# Créer un style de texte pour le texte en gras
zone_texte.tag_configure("gras", font=("Helvetica", 10, "bold"))

# Démarrer la boucle principale Tkinter
fenetre.mainloop()
