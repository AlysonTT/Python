import pickle
import tkinter as tk
from tkinter import Text, Scrollbar, Entry, Button, Label
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Vérification de l'importation du module Corpus
try:
    from Corpus import Corpus
except ImportError:
    print("Échec de l'importation du module Corpus.")

# Charger le corpus depuis le fichier
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

def effectuer_recherche():
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
        if any(mot.lower() in document.texte.lower() for mot in mots_clefs):
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
            if score_document != 0 and meilleur_resultat_affiche < 3:
                zone_texte.insert(tk.END, f"Résultat {i + 1}:\n")
                zone_texte.insert(tk.END, f"Titre du document: {document.titre}\n")
                zone_texte.insert(tk.END, f"Contenu du document:\n{document.texte}\n")
                
                # Mettre en rouge les mots-clés dans le texte du document
                for mot in mots_clefs:
                    start_index = "1.0"
                    while start_index:
                        start_index = zone_texte.search(mot, start_index, tk.END)
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
    # Effacer le contenu précédent du widget de texte
    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)

    # Afficher l'ensemble du corpus
    for document in corpus.id2doc.values():
        zone_texte.insert(tk.END, f"Titre du document: {document.titre}\n")
        zone_texte.insert(tk.END, f"Contenu du document:\n{document.texte}\n")
        zone_texte.insert(tk.END, "=" * 150 + "\n")

    # Désactiver la modification de la zone de texte
    zone_texte.config(state=tk.DISABLED)

    # Défiler vers le bas pour afficher le contenu ajouté
    zone_texte.see(tk.END)

# Créer une nouvelle fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Recherche de documents")

# Ajouter un libellé (Label) au-dessus de la barre de recherche
label_python = Label(fenetre, text="Python", font=("Helvetica", 30))
label_python.pack(pady=10)

# Créer un champ de texte (Entry) pour les mots-clés
entry_mots_clefs = Entry(fenetre, width=40)
entry_mots_clefs.pack(pady=10)

# Créer un bouton pour effectuer la recherche
bouton_recherche = Button(fenetre, text="Rechercher", command=effectuer_recherche)
bouton_recherche.pack(pady=5)

# Créer un bouton pour afficher tout le corpus
bouton_afficher_corpus = Button(fenetre, text="Afficher Tout le Corpus", command=afficher_corpus)
bouton_afficher_corpus.pack(pady=5)


# Créer un widget de texte pour afficher le contenu
zone_texte = Text(fenetre, wrap=tk.WORD, width=80, height=20)
zone_texte.pack(expand=True, fill='both')

# Configurer le style de texte pour la couleur rouge
zone_texte.tag_configure("rouge", foreground="red")

# Créer une barre de défilement
barre_defilement = Scrollbar(fenetre, command=zone_texte.yview)
barre_defilement.pack(side=tk.RIGHT, fill=tk.Y)

# Configurer la zone de texte pour utiliser la barre de défilement
zone_texte.config(yscrollcommand=barre_defilement.set)


# Démarrer la boucle principale Tkinter
fenetre.mainloop()
