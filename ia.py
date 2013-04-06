#-*- coding: utf-8 -*-
# Les fonctions de l'ia
# ...

import couleurs
import moteur
import persistance
from random import choice # faire un choix aléatoire dans une liste 

def generer_code_aleatoire ():
	""" Génère un code aléatoire, complètement

		@return : list of couleurs (Français)
	"""

	sortie = [] # le tableau de sortie 

	# On récupère la liste des couleurs possibles
	lst = couleurs.liste_couleurs ()

	# On récupère le nombre de cases demandées
	n = persistance.get_propriete ("config","nombre_cases")

	# On définit n couleurs au hasard ... 
	for i in range (n):
		sortie.append (choice (lst))
	
	return sortie

def definir_code_aleatoire ():
	""" Définit le code à trouver pour la partie 
		de mastermind, de manière aléatoire 

		@return : None
	"""
	# BRUTE FORCE !!!!
	condition = True
	while condition:
		r = moteur.definir_code (generer_code_aleatoire ())
		if r != False:
			condition = False
	
