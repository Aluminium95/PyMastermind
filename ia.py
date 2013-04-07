#-*- coding: utf-8 -*-
# Les fonctions de l'ia
# ...

import couleurs
import moteur
import iconsole
import persistance
from random import choice # faire un choix aléatoire dans une liste 

def generer_couleurs_aleatoires ():
	""" Génère un code aléatoire de couleurs, complètement !

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
	# On crée des listes aléatoires 
	# et on teste, jusqu'au jour où
	# le code secret proposé est valide 
	# par rapport à la difficulté 
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
	
		# On affiche que si le coup était valide
		# (sinon on a plein de trucs nuls :-P)
		if r != False:
			iconsole.afficher ("IA", "Joue {0} -> {1}".format (prop,r))

		if r == "perdu" or r == "gagne":
			return
