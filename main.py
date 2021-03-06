#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
# Lanceur du mastermind 
# Initialise les modules 
# et fait la boucle 
# principale du jeu

import persistance
import affichage
import moteur
import iconsole
import joueur
import ia
import couleurs
import regles

import primitives 
import chargement 

from time import sleep
from random import random

if __name__ == '__main__':
	## Arguments en ligne de commande

	import argparse

	# TODO:
	# 	-c IA | Joueur # qui code
	#	-j IA | Joueur # qui joue
	# (j dépend de c, mais pas réciproquement)
	#   --console # entièrement en console
	#   --graphique # entièrement graphique

	parser = argparse.ArgumentParser ("pymastermind")
	parser.add_argument ("-d") # Mauvais ....
	args = parser.parse_args ()
	# print (args)

	## fin arguments en ligne de commande

	iconsole.init () # Initialise le module iconsole
	
	iconsole.afficher ("Programme", "Bienvenue dans le mastermind !")
	sleep (1)
	
	# Initialisations des modules dans le bon ordre !
	persistance.init ()
	iconsole.afficher ("Chargement", "Charge la persistance ...")
	sleep (random ())
	
	couleurs.init ()
	iconsole.afficher ("Chargement", "Charge les couleurs ...")
	sleep (random ())
	
	primitives.init ()
	affichage.init ()
	iconsole.afficher ("Chargement", "Initialise l'affichage ...")
	sleep (random ())
	
	moteur.init ()
	iconsole.afficher ("Chargement", "Initialise le moteur ...")
	sleep (random ())
	
	iconsole.afficher ("Chargement", "Création des modes de l'IA ...")
	sleep (random ())
	
	iconsole.afficher ("Chargement", "Interface console principale ...")
	sleep (random ())
	
	iconsole.afficher ("Chargement", "Lancement ...")
	sleep (1)

	e = "Menu" # L'état de base est le "Menu"
	joueur.init () # Initialise le joueur 

	iconsole.afficher (e, "Tapez « help » pour obtenir de l'aide ...")

	continuer = True
	while continuer == True:
		# Les commandes sont 
		# help, humain-code, humain-joue, quit, ia-joue, ia-code
		rep = iconsole.demander (e,"Commande")
		
		if rep == "quit":
			continuer = False
			iconsole.afficher ("Programme", "Quitte ...")
		else:
			try:
				e = joueur.send (rep)
			except joueur.ErreurFatale:
				iconsole.afficher ("Programme", "Une erreur fatale est survenue ...")
				continuer = False
			except joueur.LeProgrammeurEstCon:
				iconsole.afficher ("Programme", "Une des fonctions dans `joueur.py` est mal utilisée ... quitte")
				continuer = False
			except joueur.EcranInvalide:
				iconsole.afficher ("Programme", "Le programmeur a fait une erreur dans la définition des écrans .. quitte")
				continuer = False
			except joueur.EtatInvalide:
				iconsole.afficher ("Programme", "Le programmeur s'est trompé dans les États ... erreur fatale quitte")
				continuer = False
			except persistance.CleInvalide:
				iconsole.afficher ("Programme", "Une clé est invalide ... il y a une erreur grave ... quitte")
				continuer = False
			except persistance.FichierInvalide:
				iconsole.afficher ("Programme", "Un fichier est manquant ... c'est impossible : quitte")
				continuer = False
			except persistance.ValeurInvalide:
				iconsole.afficher ("Programme", "Valeur invalide ... la configuration est corompue : quitte")
				continuer = False
			# Les autres erreurs tuent le programme avec un message, qui permet le debug, mais aussi
			# de montrer que oulala, c'est un gros programme

	try:
		persistance.save ()
	except persistance.EcritureImpossible:
		iconsole.afficher ("Erreur", "Il est impossible de sauvgarder les modifications de paramètres ...")
	# peut-il y avoir d'autres erreurs ?
