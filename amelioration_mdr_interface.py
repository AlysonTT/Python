import tkinter as tk
from tkinter import Text, Scrollbar, Entry, Button, Label, messagebox
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import re
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
liste_auteurs = set()

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

#fonction pour savoir quel auteurs ont été sélectionné
def auteurs_selection():
    auteurs_selectionnes = [listebox_auteurs.get(i) for i in listebox_auteurs.curselection()]
    if auteurs_selectionnes:
        return ", ".join(auteurs_selectionnes)
    else:
        return "null"

def est_date_valide(annee, mois, jour):
    # Vérification de l'année (entre 1900 et 2024)
    if not (1900 <= annee <= 2024):
        return False

    # Vérification du mois (entre 1 et 12)
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

#fonction pour effectuer une recherche avec des mots-clés
#un type de source ou des auteurs spécifiés ou non  
def effectuer_recherche():
    #Recuperer le type de source selectionne
    type = checkbutton_selection()

    #Recuperer les auteurs selectionnes
    auteurs = auteurs_selection() 

    #Recuperer la date entrez
    date_entre = entry_date.get().strip()

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
    
    # Vérifier qu'il y a une seule date
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
    elif len(date_lenght) > 1:
        # Afficher un message d'erreur si la date n'est pas dans le bon format
        messagebox.showerror("Erreur", "Veuillez entrer une date.")
    
    #liste des auteurs selectionne
    liste_auteurs_choisi = auteurs.split(',')

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
                if type_auteur==True and (type == "null" or type.lower() in document.url.lower()) and (date_entre == document.date or date_entre == []):
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
            #if score_document != 0 and meilleur_resultat_affiche < 3:
            #if meilleur_resultat_affiche < 3:
            if (score_document != 0 or meilleur_resultat_affiche < 3) and (mots_trouves_titre or meilleur_resultat_affiche < 3):

                zone_texte.insert(tk.END, f"Résultat {i + 1} :\n", "gras")
                zone_texte.insert(tk.END, f"Titre du document : {document.titre}\n", )
                zone_texte.insert(tk.END, f"Date du document : {document.date}\n")
                zone_texte.insert(tk.END, f"Auteurs du document: {''.join(document.auteur)}\n")
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
                start_index = "1.0"
                while start_index:
                    start_index = zone_texte.search(date_entre, start_index, tk.END, nocase=True)
                    if start_index:
                        end_index = f"{start_index}+{len(date_entre)}c"
                        zone_texte.tag_add("vert", start_index, end_index)
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

       # Supprimer les espaces avant et après chaque nom dans les deux listes
        liste_auteurs_choisi = [auteur.strip() for auteur in liste_auteurs_choisi]
        liste_auteurs_doc = [auteur.strip() for auteur in liste_auteurs_doc]

        #on regarde si un des auteurs a écrit le document
        for auteur in liste_auteurs_doc:
            if auteur in liste_auteurs_choisi:
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
            zone_texte.insert(tk.END, f"Date du document : {document.date}\n")
            zone_texte.insert(tk.END, f"Auteurs du document: {''.join(document.auteur)}\n")
            zone_texte.insert(tk.END, f"Type du document: {document.url}\n")
            if document.texte  != "":
                #si le doc est vide ne pas écrire
                zone_texte.insert(tk.END, f"Contenu du document :\n{document.texte}\n")
            zone_texte.insert(tk.END, "=" * 150 + "\n")


        # Mettre en bleu les auteurs selectionnés
        for auteur in liste_auteurs_choisi:
            start_index = "1.0"
            while start_index:
                start_index = zone_texte.search(auteur, start_index, tk.END, nocase=True)
                if start_index:
                    end_index = f"{start_index}+{len(auteur)}c"
                    zone_texte.tag_add("bleu", start_index, end_index)
                    start_index = end_index
    
    
    # Activer la modification de la zone de texte
    zone_texte.config(state=tk.DISABLED)

def configurer_barre_defilement(event):
    zone_texte.yview_scroll(-1 * (event.delta // 120), "units")

# Fonction pour traiter la date et générer la frise temporelle
def generer_frise_temporelle():
    mot_recherche = entry_mot_temporel.get()

    # Vérifier qu'il y a un seul mot
    mots = mot_recherche.strip().split()
    if len(mots) == 1:
        # On va recuperer les donnees temporelle du mot entrez par l'utilisateur
        informations_temporelles = corpus.extraire_informations_temporelles(mot_recherche)
            
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
        messagebox.showerror("Erreur", "Veuillez entrer un seul mot.")


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

#Espace pour ecrire une date
# Ajouter une étiquette
label_date = Label(fenetre, text="Veuillez entrer la date (AAAA/MM/JJ) :")
label_date.pack(pady=5)
# Créer un champ de texte (Entry) pour la date
entry_date = Entry(fenetre, width=40)
entry_date.pack(pady=10)

# Créer une barre de défilement sur le côté du cadre
barre_defilement = Scrollbar(cadre_texte, command=zone_texte.yview)
barre_defilement.pack(side=tk.RIGHT, fill=tk.Y)

# Configurer la zone de texte pour utiliser la barre de défilement
zone_texte.config(yscrollcommand=barre_defilement.set)

# Créer un champ de texte (Entry) pour le mot ou on veut avoir sa frise temporelle
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