from Classes_filles import RedditDocument, ArxivDocument

#TD5 SIGLETON

def singleton(cls): 
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    return wrapper

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