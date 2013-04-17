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

def gen_main_fsm ():
	""" Retourne le générateur de la boucle principale !
		
		@return : generator
	"""
	etat = "Menu"
	# Variables 
	code_defini = False
	
	# On commence la boucle infinie !
	while True:
		r = (yield etat) # Récupère le message (et retourne l'état)
		
		if rep == "help":
			iconsole.afficher (etat,"Les commandes sont : \n\t - « help » \n\t - « regles » \n\t - « humain-code » \n\t - « humain-joue » \n\t - « quit » \n\t - « ia-code » \n\t - « ia-joue » \n\t - « modifier-theme » \n\t - « modifier-niveau »")
		elif rep == "quit":
			continuer = False
		elif rep == "regles":
			primitives.raz ()
			chargement.run (1,"ligne")
			primitives.raz ()
			regles.regles_normal ("#AAA")
		
		if etat == "Menu":
			if rep == "ia-code":
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
			elif rep == "modifier-theme":
				etat = "Theme"
			elif rep == "modifier-niveau":
				etat = "Niveau"
			else:
				iconsole.afficher (etat,"Cette requête est invalide ...")
		elif etat == "Theme":
			if rep == "list":
				iconsole.afficher (etat,"Voici la liste des thèmes : 1,2,3,4 ... et oui c'est nul")
			elif rep == "fin":
				iconsole.afficher (etat,"Theme modifié ... ")
				etat = "Menu"
			else:
				iconsole.afficher (etat,"Selection theme : " + rep)
		elif etat == "Niveau":
			if rep == "list":
				iconsole.afficher (etat,"Voici la liste des niveaux : .... ")
			elif rep == "fin":
				iconsole.afficher (etat,"Niveau modifié pour la prochaine partie")
			else:
				iconsole.afficher (etat,"Vous avez sélectionné le niveau : " + rep)
		else:
			break # Erreur fatale !
		

if __name__ == '__main__':
	# Initialisations des modules dans le bon ordre !
	persistance.init ()
	couleurs.init ()
	affichage.init ()
	moteur.init ()
	
	iconsole.afficher ("Programme", "Bienvenue dans le mastermind !")

	machine = gen_main_fsm ()

	e = machine.next () # récupère l'état 
	
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
			e = machine.send (rep) 

	persistance.save ()
