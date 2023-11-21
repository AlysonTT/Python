from Classes_filles import RedditDocument, ArxivDocument

# Factory pour créer des documents
class DocumentFactory:
    def create_document(self, doc_type, **kwargs):
        if doc_type == "Reddit":
            return RedditDocument(**kwargs)
        elif doc_type == "Arxiv":
            return ArxivDocument(**kwargs)
        else:
            raise ValueError(f"Type de document non pris en charge : {doc_type}")
 
# Exemple d'utilisation du Factory Pattern
factory = DocumentFactory()

reddit_doc = factory.create_document("Reddit", titre="Titre Reddit", auteur="Auteur Reddit", nb_com=10)
arxiv_doc = factory.create_document("Arxiv", titre="Titre Arxiv", auteur="Auteur Arxiv", co_auteurs="Co-Auteur Arxiv")

print(reddit_doc)
print(arxiv_doc)