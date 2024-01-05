import pickle
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

while True:
    # Etape 1 : demander à l'utilisateur d'entrer quelques mots-clefs
    mots_clefs = input("Entrez quelques mots-clés (séparés par des espaces) : ").split()

    # Vérifier si l'utilisateur souhaite quitter
    if 'q' in [mot.lower() for mot in mots_clefs]:
        print("Merci d'avoir utilisé le moteur de recherche. Au revoir!")
        break

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

    # Afficher les trois meilleurs résultats (avec score non nul)
    meilleur_resultat_affiche = 0
    for i, (document, score_document) in enumerate(documents_retrouves):
        if score_document != 0 and meilleur_resultat_affiche < 3:
            print(f"Résultat {meilleur_resultat_affiche + 1}:")
            print(f"Titre du document: {document.titre}")
            print(f"Contenu du document:\n{document.texte}")
            print(f"Score de similarité: {score_document}")
            print("=" * 50)
            meilleur_resultat_affiche += 1