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

def afficher_aide (etat):
	# Commandes : un gros dictionnaire avec l'aide :-)  
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
			"proposer" : "Permet de faire une proposition, si et seulement si le plateau est affiché",
			"plateau" : "Permet de réafficher le plateau de jeu",
			"score" : "Permet de savoir le score actuel", # Pour l'instant c'est faux
			"abandon" : "Permet de revenir au menu, et abandonner la partie"
		}
	}
	
	# On affiche manuellement des trucs ... c'est MAAAAAL
	def gen_help ():
		yield "Commandes globales ..."
		for i,j in aide["global"].items ():
			yield ("\t" + i,j)
		
		yield "Commandes d'état"
		for i,j in aide[etat].items ():
			yield ("\t" + i,j)
	iconsole.afficher_generateur (etat, "Aide : ", gen_help ())
	

def gen_main_fsm ():
	""" Retourne le générateur de la boucle principale !
		
		@return : generator
	"""
	
	class State:
		def __init__ (self,initial):
			self.etat = initial
			
		def get (self):
			return self.etat

		def set (self,valeur):
			self.etat = valeur
			
			iconsole.separateur ()
			iconsole.afficher (valeur, "Vous êtes maintenant dans un nouveau mode")
			afficher_aide (valeur)

	objet_etat = State ("Menu")
	# etat = "Menu" # Etat = Menu | Niveau | Theme | Humain-Joue
	
	
	
	# Variables Menu
	code_defini = False
	# Variables Humain-Joue
	plateau_affiche = True

	# On commence la boucle infinie !
	while True:
		etat = objet_etat.get ()
		r = (yield etat) # Récupère le message (et retourne l'état)
		
		# Magnifique ÉNORME switch ... 
		# le principe est de récupérer la commande, et 
		# de regarder l'état actuel ... et faire des actions 
		# en fonction :)
		if rep == "help": # Commande indépendante de l'état courant !
			afficher_aide (etat)
		elif rep == "regles": # Commande indépendante de l'état courant !
			iconsole.afficher (etat, "Affichage des règles sur la fenêtre graphique ...")
			chargement.run (2,"ligne")
			regles.regles_mode (moteur.get_mode ())
			plateau_affiche = False
		elif rep == "scores": # Commande indépendante de l'état courant !
			iconsole.afficher (etat, "Affichage des scores sur la fenêtre graphique ...")
			# primitives.raz ()
			affichage.high_score ()
		elif rep == "score": # Euh ... elle est censée être disponible uniquement localement ... 
			iconsole.afficher (etat, moteur.calcul_score ())
		elif etat == "Menu": # MENU
			if rep == "ia-code":
				iconsole.afficher (etat, "L'IA va choisir un code")
				chargement.run (5,"ligne")
				primitives.raz ()
				ia.choisir_code ()
				code_defini = True
				iconsole.afficher (etat, "L'IA a déterminé un code")
			elif rep == "humain-code":
				iconsole.afficher (etat, "L'humain va choisir un code")
				iconsole.afficher (etat, "Le niveau actuel est : " + moteur.get_mode ())
				iconsole.afficher_liste (etat, "Les couleurs disponibles sont : ", couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs ()])
				joueur.choisir_code ()
				code_defini = True
				iconsole.afficher (etat, "L'humain a déterminé un code")
			elif rep == "humain-joue" and code_defini == True:
				chargement.run (10,"arc")
				affichage.reset ()
				#
				# joueur.jouer ()
				plateau_affiche = True
				moteur.restant = 10 # Moche !
				objet_etat.set ("Humain-Joue")
				
				iconsole.afficher (etat, "Le niveau actuel est : " + moteur.get_mode ())
				iconsole.afficher_liste (etat, "Les couleurs disponibles sont : ", couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs ()])
			elif rep == "ia-joue" and code_defini == True:
				iconsole.afficher (etat, "L'IA va jouer une partie")
				chargement.run (5,"cercle")
				affichage.reset ()
				ia.jouer ("aleatoire")
				moteur.restant = 10 # Moche !
			elif rep == "theme":
				objet_etat.set ("Theme")
			elif rep == "niveau":
				objet_etat.set ("Niveau")
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
				objet_etat.set ("Menu")
			else:
				try:
					affichage.choix_theme (int (rep)) # un truc qui peut facilement planter 
					iconsole.afficher (etat,"Selection theme : " + rep)
					primitives.raz ()
					path = "Images/Theme" + rep + "/fond.gif"
					primitives.bgpic (path)
				except:
					iconsole.afficher (etat,"... ce theme est invalide ")
		elif etat == "Niveau": # NIVEAU ....
			if rep == "list":
				iconsole.afficher (etat, str (moteur.get_liste_modes ()))
			elif rep == "actuel":
				iconsole.afficher (etat, moteur.get_mode ())
			elif rep == "fin":
				iconsole.afficher (etat,"Niveau modifié pour la prochaine partie")
				objet_etat.set ("Menu")
			else:
				if rep in (moteur.get_liste_modes ()):
					iconsole.afficher (etat,"Vous avez sélectionné le niveau : " + rep)
					moteur.set_mode (rep)
					regles.regles_mode (rep) # affiche les règles 
				else:
					iconsole.afficher (etat,"Ce niveau est invalide ...")
		elif etat == "Humain-Joue": # HUMAIN-JOUE
			if rep == "abandon": # Abandon de la partie -> retour au menu
				iconsole.afficher (etat,"Vous avez abandonné la partie ...")
				objet_etat.set ("Menu")
			if rep == "plateau":
				iconsole.afficher (etat,"Le plateau est affiché, vous pouvez proposer des solutions")
				moteur.reprendre_partie ()
			elif rep == "proposer" and plateau_affiche == True:
				Li = iconsole.demander_tableau ()
				try:
					r = moteur.verification_solution (Li)
					if r == "gagne":
						iconsole.afficher (etat, "Vous avez gagné !!!")
						objet_etat.set ("Menu")
					elif r == "perdu":
						iconsole.afficher (etat,"Vous avez perdu !!!")
						objet_etat.set ("Menu")
					elif r == False:
						iconsole.afficher (etat, "Votre proposition n'a pas de sens ...")
					else:
						a,b = r
				
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
				except moteur.TableauInvalide as exception:
					iconsole.afficher (etat, "Le tableau est invalide : {0}".format (exception.message))
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
	
	try:
		persistance.save ()
	except persistance.EcritureImpossible:
		iconsole.afficher ("Erreur", "Il est impossible de sauvgarder les modifications de paramètres ...")
