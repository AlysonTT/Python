from Classes import Document

class RedditDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="",numDoc="",nb_com=0):
        super().__init__(titre=titre, auteur=auteur, date=date, url=url, texte=texte, numDoc=numDoc)
        self.nb_com=nb_com

    def getNbCom(self):
        return self.nb_com

    def setNbCom(self, nb_com):
        self.nb_com=nb_com

    def __str__(self):
        return f"Source: {self.getType()} \t# Auteur : {self.auteur}\t# titre : {self.titre}\t# nombres de commentaires : {self.nb_com}"

    def getType(self):
        return self.__class__.__name__

class ArxivDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="",numDoc="",co_auteurs=""):
        super().__init__(titre=titre, auteur=auteur, date=date, url=url, texte=texte,numDoc=numDoc)
        self.co_auteurs=co_auteurs

    def getCoAuteurs(self):
        return self.__co_auteurs

    def setCoAuteurs(self, co_auteurs):
        self.__co_auteurs=co_auteurs

    def __str__(self):
        return f"Source: {self.getType()} \t# Co-Auteur : {self.co_auteurs}\t# titre : {self.titre}"

#TD5 : 3.2
    def getType(self):
        return self.__class__.__name__