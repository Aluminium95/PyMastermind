#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# Lopez Aliaume
# 30/03/2013
#
# Un utilitaire de modification
# des fichiers de configuration
#
# TODO:
#	- utilisation du module fsm 
#		Démonstration de l'utilisation du module FSM
#		création des états 
#		des variables globales
#		des transitions
#
#
# Ce code a pour vocation d'être simple 
# et compréhensible, afin de servir de modèle
# pour l'utilisation des modules « persistance »
# et « fsm » de mon cru !
#
#
# Chaque ligne de code est comméntée le mieux possible,
# afin de vous permettre de comprendre les buts et 
# moyens !
#
#
# OBJECTIF: permettre l'édition par un programme des 
# 	variables de configuration, écrites dans des fichiers
# 	« illisibles » par l'utilisateur normal ... Permettant
# 	ainsi de configurer des comportements, en utilisant un 
#	outil adapté, qui empêche de faire n'importe quoi

import persistance
# import iconsole


# On se demande comment gérer la navigation parmis 
# les différents fichiers de configuration ...
# on fait ainsi une fonction qui permet de choisir un
# fichier ...

def selection_fichier ():
	continuer = True
	while continuer:
		# On demande un fichier ...
		fichier = iconsole.demander ("selection fichier","Fichier ou « list »")

		if fichier == "list": # Si l'utilisateur demande une liste !
			print persistance.liste_fichiers ()
		else: 
			# Ici, il faudrait par exemple utiliser la fonction 
			# « persistance.new_file » qui crée un nouveau fichier 
			# s'il n'existe pas ... 
			return fichier # Sinon on suppose que c'est un fichier ...
			
# Lance ce bout de code Si et Seulement Si
# le fichier est lancé par l'utilisateur !
# exemple : quand on génère la doc, ça ne compte pas !
if __name__ == "__main__":
	# Il est nécessaire d'initialiser persistance
	# une seule et unique fois par programme ...
	# or ceci est un programme indépendant, il faut 
	# donc initialiser persistance avec la fonction :

	persistance.init () # initialise la configuration 
	# On part avec un fichier demandé à l'utilisateur 
	f = selection_fichier ()
	continuer = "o" # Tant que l'on doit continuer 
	while continuer == "o":
	
		c = True
		variable = ""
		while c:
			# On demande quelle variable sélectionner 
			variable = iconsole.demander ("selection variable","Variable, « list » ou « up »")
		
			# On peut afficher la liste des variables 
			# du fichier courant 
			if variable == "list":
				print persistance.liste_variables (f)
			elif variable == "up":
				# sélectionner un nouveau fichier 
				f = selection_fichier ()
			else:
				# où alors, c'est bel et bien une variable ... 
				c = False
		
		# On doit afficher la valeur actuelle ... au cas où
		print "Valeur actuelle : ", persistance.get_propriete (f,variable)
	
		# Et définir une nouvelle valeur de remplacement
		val = iconsole.demander ("selection valeur","Nouvelle valeur : ")
	
		# Définir
		persistance.set_propriete (f,variable,val)
	
		# Demander si on veut réitérer l'opération 
		continuer = iconsole.demander ("main","Continuer (o|n) : ")

	# IMPORTANT : on sauvegarde les modifications faites 
	# VIRTUELLEMENT sur les fichiers sur le disque dur 
	# avec la fonction « save »
	persistance.save ()
