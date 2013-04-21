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
	etat = "Menu" # Etat = Menu | Niveau | Theme | Humain-Joue
	# Variables 
	code_defini = False

	# Commandes 
	aide = {
		"global" : {
			"quit" : "Quitte le programme ...",
			"regles" : "Affiche les règles du jeu ...",
			"scores" : "Affiche les meilleurs scores du jeu ...",
			"score" : "Affiche le score actuel ..."
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
			"fin" : "Enregistre le niveau sélectionné et revient au menu",
			"@" : "Une autre chaine de caractère est prise comme un niveau"
		},
		"Theme" : {
			"list" : "Fait la liste des thèmes disponibles",
			"actuel" : "Affiche le thème actuel ...",
			"fin" : "Engeristre le thème sélectionné et revient au menu",
			"@" : "Sélectionne le texte rentré comme un thème"
		},
		"Humain-Joue" : {
			"proposer" : "Permet de faire une proposition",
			"score" : "Permet de savoir le score actuel", # Pour l'instant c'est faux
			"abandon" : "Permet de revenir au menu, et abandonner la partie"
		}
	}
	
	# On commence la boucle infinie !
	while True:
		r = (yield etat) # Récupère le message (et retourne l'état)
		
		if rep == "help":
			iconsole.afficher (etat,"Aide :")
			# On affiche manuellement des trucs ... c'est MAAAAAL
			def gen_help ():
				yield "Commandes globales ..."
				for i,j in aide["global"].items ():
					yield ("\t" + i,j)
				
				yield "Commandes d'état"

				for i,j in aide[etat].items ():
					yield ("\t" + i,j)
			iconsole.afficher_generateur (etat, "Aide : ", gen_help ())
		elif rep == "quit":
			continuer = False
		elif rep == "regles":
			primitives.raz ()
			chargement.run (2,"ligne")
			primitives.raz ()
			regles.regles_normal ("#AAA")
		elif rep == "scores":
			primitives.raz ()
			affichage.high_score ()
		elif rep == "score":
			iconsole.afficher (etat, moteur.calcul_score ())
		elif etat == "Menu":
			if rep == "ia-code":
				ia.choisir_code ()
				code_defini = True
			elif rep == "humain-code":
				joueur.choisir_code ()
				code_defini = True
			elif rep == "humain-joue" and code_defini == True:
				iconsole.separateur ()
				primitives.raz ()
				chargement.run (10,"arc")
				affichage.reset ()
				#
				# joueur.jouer ()
				moteur.restant = 10 # Moche !
				etat = "Humain-Joue"
			elif rep == "ia-joue" and code_defini == True:
				primitives.raz ()
				chargement.run (5,"cercle")
				affichage.reset ()
				ia.jouer ("knuth")
				moteur.restant = 10 # Moche !
			elif rep == "theme":
				iconsole.separateur ()
				iconsole.afficher (etat, "Vous êtes dans le mode « Theme »")
				etat = "Theme"
			elif rep == "niveau":
				iconsole.separateur ()
				iconsole.afficher (etat, "Vous êtes dans le mode « Niveau »")
				etat = "Niveau"
			else:
				iconsole.afficher (etat,"Cette requête est invalide ...")
		elif etat == "Theme": # THÈME ......
			if rep == "list":
				def gen_liste_theme ():
					for i in affichage.liste_themes ():
						desc = persistance.get_propriete ("backgrounds", "theme:" + i + ":description")
						yield (i,desc)

				iconsole.afficher_generateur (etat,"Themes",gen_liste_theme ())
			elif rep == "fin":
				iconsole.afficher (etat,"Theme modifié ... ")
				etat = "Menu"
				iconsole.separateur ()
				iconsole.afficher (etat, "Vous êtes dans le mode « Menu »")
			else:
				try:
					affichage.choix_theme (int (rep)) # un truc qui peut facilement planter 
					iconsole.afficher (etat,"Selection theme : " + rep)
				except:
					iconsole.afficher (etat,"... ce theme est invalide ")
		elif etat == "Niveau": # NIVEAU ....
			if rep == "list":
				iconsole.afficher (etat, str (moteur.get_liste_modes ()))
			elif rep == "actuel":
				iconsole.afficher (etat, moteur.get_mode ())
			elif rep == "fin":
				iconsole.afficher (etat,"Niveau modifié pour la prochaine partie")
				etat = "Menu"
				iconsole.separateur ()
				iconsole.afficher (etat, "Vous êtes dans le mode « Menu »")
			else:
				if rep in (moteur.get_liste_modes ()):
					iconsole.afficher (etat,"Vous avez sélectionné le niveau : " + rep)
					moteur.set_mode (rep)
				else:
					iconsole.afficher (etat,"Ce niveau est invalide ...")
		elif etat == "Humain-Joue":
			if rep == "abandon":
				etat = "Menu"
			elif rep == "proposer":
				Li = iconsole.demander_tableau()
				r = moteur.verification_solution (Li)
				if r == "gagne":
					iconsole.afficher (etat, "Vous avez gagné !!!")
					etat = "Menu"
				elif r == "perdu":
					iconsole.afficher (etat,"Vous avez perdu !!!")
					etat = "Menu"
				elif r == False:
					iconsole.afficher (etat, "Votre proposition n'a pas de sens ...")
				else:
					a,b = r
					print ("_" * 50) # Afficher à la main ?
			
					# On fait un joli affichage qui dit si on doit mettre un S ou pas ...
					sa = ""
					sb = ""

					if a > 1:
						sa = "s"

					if b > 1:
						sb = "s"
			
					messaga = "Il y a {0} bonne{1} couleur{1} bien placée{1}".format (a,sa)
					messagb = "Il y a {0} bonne{1} couleur{1} mal placée{1}".format (b,sb)

					iconsole.afficher(etat, messaga)
					iconsole.afficher(etat, messagb)
					iconsole.afficher(etat, "Voulez-vous rejouer")
					print ("_" * 50) # Idem ? ...
			else:
				iconsole.afficher (etat, "Requête invalide ...")
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

	# Code en python2
	# e = machine.next () # récupère l'état 
	e = next (machine) # Code en python3

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
