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
	etat = "Menu" # Etat = Menu | Niveau | Theme
	# Variables 
	code_defini = False

	# Commandes 
	aide = {
		"global" : {
			"quit" : "Quitte le programme ...",
			"regles" : "Affiche les règles du jeu ...",
			"scores" : "Affiche les meilleurs scores du jeu ..."
		},
		"Menu" : {
			"ia-code" : "Fait décider un code à trouver par une IA",
			"ia-joue" : "Fait trouver le code par une IA (nécessite qu'un code ai été défini avant)",
			"humain-code" : "Fait rentrer un code à l'utilisateur",
			"humain-joue" : "Fait trouver le code à l'utilisateur",
			"theme" : "Permet à l'utilisateur de chosir un thème",
			"niveau" : "Permet à l'utilisateur de changer de niveau de difficulté"
		},
		"Niveau" : {
			"list" : "Fait la liste des niveaux disponibles",
			"actuel" : "Affiche le niveau actuel de difficulté",
			"end" : "Enregistre le niveau sélectionné et revient au menu",
			"@" : "Une autre chaine de caractère est prise comme un niveau"
		},
		"Theme" : {
			"list" : "Fait la liste des thèmes disponibles",
			"actuel" : "Affiche le thème actuel ...",
			"end" : "Engeristre le thème sélectionné et revient au menu",
			"@" : "Sélectionne le texte rentré comme un thème"
		}
	}
	
	# On commence la boucle infinie !
	while True:
		r = (yield etat) # Récupère le message (et retourne l'état)
		
		if rep == "help":
			iconsole.afficher (etat,"Aide :")
			# On affiche manuellement des trucs ... c'est MAAAAAL
			print "\t ## Commandes Globales ##"
			for i,j in aide["global"].items ():
				print "\t - ",i, ":"
				print "\t\t",j
			print "\t ## Commandes", etat, "##"
			for i,j in aide[etat].items ():
				print "\t - ",i, ":"
				print "\t\t",j

		elif rep == "quit":
			continuer = False
		elif rep == "regles":
			primitives.raz ()
			chargement.run (1,"ligne")
			primitives.raz ()
			regles.regles_normal ("#AAA")

		elif etat == "Menu":
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
			elif rep == "theme":
				etat = "Theme"
			elif rep == "niveau":
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
				affichage.choix_theme (int (rep)) # un truc qui peut facilement planter 
				iconsole.afficher (etat,"Selection theme : " + rep)
		elif etat == "Niveau":
			if rep == "list":
				iconsole.afficher (etat, str (moteur.get_liste_modes ()))
			elif rep == "actuel":
				iconsole.afficher (etat, moteur.get_mode ())
			elif rep == "fin":
				iconsole.afficher (etat,"Niveau modifié pour la prochaine partie")
				etat = "Menu"
			else:
				if rep in (moteur.get_liste_modes ()):
					iconsole.afficher (etat,"Vous avez sélectionné le niveau : " + rep)
					moteur.set_mode (rep)
				else:
					iconsole.afficher (etat,"Ce niveau est invalide ...")
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
