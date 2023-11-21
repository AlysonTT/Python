# Correction de G. Poux-Médard, 2021-2022

#TD5 SIGLETON

def singleton(cls): 
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    return wrapper

# =============== 2.1 : La classe Document ===============
#@singleton
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

# =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"

    #TD5 fct type
    def getType(self):
        return self.type
        #pass

# =============== 2.4 : La classe Author ===============
class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
# =============== 2.5 : ADD ===============
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
    
#TD5
'''
class RedditDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="",nb_com=0):
        super().__init__(titre=titre, auteur=auteur, date=date, url=url, texte=texte)
        self.nb_com=nb_com

    def getNbCom(self):
        return self.nb_com

    def setNbCom(self, nb_com):
        self.nb_com=nb_com

    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}\t# nombres de commentaires : {self.nb_com}"

    def getType(self):
        return self.__class__.__name__

class ArxivDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="",co_auteurs=""):
        super().__init__(titre=titre, auteur=auteur, date=date, url=url, texte=texte)
        self.co_auteurs=co_auteurs

    def getCoAuteurs(self):
        return self.__co_auteurs

    def setCoAuteurs(self, co_auteurs):
        self.__co_auteurs=co_auteurs

    def __str__(self):
        return f"Co-Auteur : {self.co_auteurs}\t# productions : {self.ndoc}"

    def getType(self):
        return self.__class__.__name__
'''