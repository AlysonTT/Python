from Classes import Document

# Définition de la classe RedditDocument, héritant de la classe Document
class RedditDocument(Document):
    # Constructeur de la classe, initialisation des attributs
    def __init__(self, titre="", auteur="", date="", url="", texte="",numDoc="",nb_com=0):
        super().__init__(titre=titre, auteur=auteur, date=date, url=url, texte=texte, numDoc=numDoc)
        self.nb_com=nb_com
    
    # Fonction pour récupérer le nombre de commentaires
    def getNbCom(self):
        return self.nb_com

    # Fonction pour définir le nombre de commentaires
    def setNbCom(self, nb_com):
        self.nb_com=nb_com

    # Fonction pour afficher une représentation textuelle de l'objet
    def __str__(self):
        return f"Source: {self.getType()} \t# Auteur : {self.auteur}\t# titre : {self.titre}\t# nombres de commentaires : {self.nb_com}"

    # Fonction pour obtenir le type de document (RedditDocument dans ce cas)
    def getType(self):
        return self.__class__.__name__

# Définition de la classe ArxivDocument, héritant de la classe Document
class ArxivDocument(Document):
     # Constructeur de la classe, initialisation des attributs
    def __init__(self, titre="", auteur="", date="", url="", texte="",numDoc="",co_auteurs=""):
        super().__init__(titre=titre, auteur=auteur, date=date, url=url, texte=texte,numDoc=numDoc)
        self.co_auteurs=co_auteurs

    # Méthode pour récupérer la liste des co-auteurs
    def getCoAuteurs(self):
        return self.__co_auteurs

    # Méthode pour définir la liste des co-auteurs
    def setCoAuteurs(self, co_auteurs):
        self.__co_auteurs=co_auteurs

    # Méthode pour afficher une représentation textuelle de l'objet
    def __str__(self):
        return f"Source: {self.getType()} \t# Co-Auteur : {self.co_auteurs}\t# titre : {self.titre}"

    #TD5 : 3.2
    # Méthode pour obtenir le type de document (ArxivDocument dans ce cas)
    def getType(self):
        return self.__class__.__name__