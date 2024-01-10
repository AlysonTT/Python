from Classes_filles import RedditDocument, ArxivDocument
from Corpus import Corpus

# Crée des instances des classes filles
reddit_doc = RedditDocument(titre="Titre Reddit", auteur="Auteur Reddit", nb_com=10)
arxiv_doc = ArxivDocument(titre="Titre Arxiv", auteur="Auteur Arxiv", co_auteurs="Co-Auteur Arxiv")

# Crée une instance de la classe Corpus
corpus = Corpus(nom="corpus_test")
 
# Ajoutez les documents au corpus
corpus.add(reddit_doc)
corpus.add(arxiv_doc)

# Affichez les documents du corpus
# Problème dans mon affichage n'affiche que la classe arxit bien que redit soit aussi dedans
#corpus.show() 

#Affichez les documents du corpus
print(corpus)