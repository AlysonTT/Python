import tkinter as tk

class Deselection:
    def __init__(self):
        pass
    
    '''
    Désélectionne tous les éléments de la listebox des auteurs et décoche le checkbutton associé.

    Paramètres :
        - listebox_auteurs : Listebox contenant les auteurs.
        - checkbutton_deselection : Checkbutton de désélection.

    Algorithme : Utilise les méthodes appropriées pour déselectionner tous les éléments et mettre à jour l'état du checkbutton.

    '''
    def deselectionner_tous_les_auteurs(self, listebox_auteurs, checkbutton_deselection):
        # Désélectionne tous les éléments de la listebox
        listebox_auteurs.selection_clear(0, tk.END)
        # On met l'état du checkbutton en non coché
        checkbutton_deselection.deselect()

    '''
    Désélectionne tous les boutons associés aux variables d'affichage et de comparaison.

    Paramètres :
        - vars_afficher : Dictionnaire de variables associées aux boutons d'affichage.
        - vars_comparer : Dictionnaire de variables associées aux boutons de comparaison.
        
    Algorithme :
    Parcourt toutes les variables associées aux boutons d'affichage et les désélectionne.
    Parcourt toutes les variables associées aux boutons de comparaison et les désélectionne.
    '''
    def clear_tous_les_boutons(self, vars_afficher, vars_comparer):
        for var_afficher in vars_afficher.values():
            var_afficher.set(0)

        for var_comparer in vars_comparer.values():
            var_comparer.set(0)