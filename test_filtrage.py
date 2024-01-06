import tkinter as tk
from tkinter import Button

# Fonction pour mettre à jour les variables de contrôle et afficher les détails
def mise_a_jour_et_affichage(index):
    for i, var in enumerate(variables):
        value = 1 if i == index else 0
        var.set(value)
        print(f"Variable {i + 1}: {var.get()}")

# Créer une nouvelle fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Sélection Unique")

# Sources disponibles
sources = ["Source 1", "Source 2", "Source 3"]

# Variables pour stocker l'état des Checkbuttons
variables = [tk.IntVar() for _ in sources]

# Créer les Checkbuttons et les ajouter à la fenêtre
for i, option in enumerate(sources):
    checkbutton = tk.Checkbutton(fenetre, text=option, variable=variables[i], command=lambda i=i: mise_a_jour_et_affichage(i))
    checkbutton.pack(side=tk.LEFT, padx=5)

# Créer un bouton pour afficher les détails des types de sources sélectionnés
bouton_afficher_details = Button(fenetre, text="Afficher Détails", command=lambda: print("Variables actuelles:", [var.get() for var in variables]))
bouton_afficher_details.pack(pady=10)

# Démarrer la boucle principale Tkinter
fenetre.mainloop()
