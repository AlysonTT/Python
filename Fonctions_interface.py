import tkinter as tk
from tkinter import messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import re

'''Section 1 : Fonctions Utilitaires'''
'''Cette section regroupe plusieurs fonctions utilitaires 
qui facilitent la gestion des sélections d'utilisateurs, 
la validation des dates et des auteurs, etc.'''
