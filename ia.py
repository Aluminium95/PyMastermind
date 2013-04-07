#-*- coding: utf-8 -*-
# Les fonctions de l'ia
# ...

import couleurs
import moteur
import persistance
from random import choice # faire un choix aléatoire dans une liste 

def generer_couleurs_aleatoires ():
	""" Génère un code aléatoire, complètement

		@return : list of couleurs (Français)
	"""

	sortie = [] # le tableau de sortie 

	# On récupère la liste des couleurs possibles
	lst = couleurs.liste_couleurs ()

	# On récupère le nombre de cases demandées
	n = persistance.get_propriete ("config","nombre_cases")

	# On définit n couleurs au hasard ... 
	for i in xrange (int (n)):
		sortie.append (choice (lst))
	
	return sortie

def choisir_code (mode="aleatoire"):
	""" Définit le code à trouver pour la partie 
		de mastermind, de manière aléatoire 

		@return : None
	"""
	# BRUTE FORCE !!!!
	condition = True
	while condition:
		r = moteur.definir_code (generer_couleurs_aleatoires ())
		if r != False:
			condition = False

def jouer (mode = "aleatoire"):
	""" Fait jouer l'IA pour deviner le code 

		@mode : string (aleatoire | probabiliste | deterministe) = 
			le mode de résolution 

		@return : None
	"""
	# On fait pas dans la finesse ici 
	# Il faut plus de rafinement --"
	while True:
		prop = generer_couleurs_aleatoires ()
		r = moteur.proposer_solution (prop)
		
		print r

		if r == "perdu" or r == "gagne":
			return
