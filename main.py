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
	
	code_defini = False

	continuer = True
	while continuer == True:
		# Les commandes sont 
		# help, humain-code, humain-joue, quit, ia-joue, ia-code
		rep = iconsole.demander ("Menu","Commande")
		
		if rep == "help":
			iconsole.afficher ("Menu:help","Les commandes sont : « help », « regles », « humain-code », « humain-joue », « quit », « ia-code » et « ia-joue »")
		elif rep == "quit":
			continuer = False
		elif rep == "regles":
			primitives.raz ()
			chargement.run (1,"ligne")
			primitives.raz ()
			regles.regles_normal ("#AAA")
		elif rep == "ia-code":
			ia.choisir_code ()
			code_defini = True
		elif rep == "humain-code":
			joueur.choisir_code ()
			code_defini = True
		elif rep == "humain-joue" and code_defini == True:
			primitives.raz ()
			chargement.run (2,"arc")
			affichage.reset ()
			joueur.jouer ()
			moteur.restant = 10 # Moche !
		elif rep == "ia-joue" and code_defini == True:
			primitives.raz ()
			chargement.run (1,"cercle")
			affichage.reset ()
			ia.jouer ("knuth")
			moteur.restant = 10 # Moche !
		else:
			iconsole.afficher ("Menu","Cette requête est invalide ...")

	persistance.save ()
