#-*- coding: utf-8 -*-
# 03/04/2013

import persistance
import affichage
import moteur
import iconsole
import joueur
import ia
import couleurs
import misc
import regles

import primitives 
import chargement

if __name__ == '__main__':
	# Initialisations des modules dans le bon ordre !
	persistance.init ()
	couleurs.init ()
	affichage.init ()
	moteur.init ()
	
	iconsole.afficher ("Programme", "Bienvenue dans le mastermind !")

	e = "Menu"
	machine = joueur.Mastermind (e)

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
				e = machine.send (rep)
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
			# Les autres erreurs tuent le programme avec un message, qui permet le debug, mais aussi
			# de montrer que oulala, c'est un gros programme 

	try:
		persistance.save ()
	except persistance.EcritureImpossible:
		iconsole.afficher ("Erreur", "Il est impossible de sauvgarder les modifications de paramètres ...")
	# peut-il y avoir d'autres erreurs ?
