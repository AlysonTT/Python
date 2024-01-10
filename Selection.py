class Selection:
    def __init__(self):
        pass

    #fonction qui permet d'avoir qu'un type de source selectionné
    def selection_unique(self, index, variables):
        for i, var in enumerate(variables):
            if i != index:
                var.set(0)

    '''
    Paramètres : 
        - source : Liste des sources disponibles.
        - variables : Liste de variables associées aux Checkbuttons.    

    Retourne les types de sources sélectionnés sous forme d'une chaîne, séparées par des virgules,
    sinon renvoie "null" si aucune source n'est sélectionnée.

    Algorithme : Utilise les variables des types de source pour identifier ceux qui sont sélectionnés.
    '''
    def checkbutton_selection(self, source, variables):
        options_selectionnees = [source[i] for i, var in enumerate(variables) if var.get()]
        if options_selectionnees:
            return ", ".join(options_selectionnees)
        else:
            return "null"
        
    '''
    Paramètres:
        listebox_auteurs : Listebox contenant les auteurs.

    Retourne les auteurs sélectionnés sous forme d'une chaîne, séparés par des virgules,
    sinon renvoie "null" si aucun auteur n'est sélectionné.

    Algorithme : Utilise la sélection actuelle dans la listebox des auteurs pour obtenir les auteurs sélectionnés.

    '''
    def auteurs_selection(self, listebox_auteurs):
        auteurs_selectionnes = [listebox_auteurs.get(i) for i in listebox_auteurs.curselection()]
        if auteurs_selectionnes:
            return ", ".join(auteurs_selectionnes)
        else:
            return "null"

