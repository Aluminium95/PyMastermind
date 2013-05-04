#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Fichier du joueur (némésis de ia.py)

# Charge toute l'arborescence ... on sait jamais 
import persistance
import affichage
import moteur
import iconsole
import joueur
import ia
import couleurs
import regles

import chargement
from random import randint 

from primitives import *

# DEB EXCEPTIONS

class EcranInvalide (Exception): # Un problème d'écran 
	def __init__ (self, ecran):
		self.ecran = ecran 

class EtatInvalide (Exception): # Un problème d'état
	def __init__ (self, etat):
		self.etat = etat
		
class LeProgrammeurEstCon (Exception): # Ah, c'est une mauvaise utilisation d'une fonction
	pass

class ErreurFatale (Exception): # Pas la peine de continuer ...
	pass 

# FIN EXCEPTIONS


etats = ["Menu","Humain-Joue","Theme","Niveau","Proposer-Code","Definir-Code"]
ecrans = ["plateau", "regles", "scores"]
etat = ""
ecran = "plateau" # Quel est l'écran actuel ?
tableau_tampon = []

boutons = [] # Tableau des boutons

def ajouter_bouton (nom,cote,position):
	global boutons
	boutons.append ([nom,cote,position])

def click_to_bouton (x,y):
	
	for i in boutons:
		w = i[1]
		xb,yb = i[2]
		if xb < x < xb + w and yb < y < yb + w:
			return i[0] # le nom 
		
def callback (x,y):
	print (click_to_bouton (x,y))
	
def init ():
	""" Constructeur 
		
		@initial : str = l'état de départ 
		
		@return : Mastermind 
	"""
	set_etat ("Menu")
	set_ecran ("plateau")
	
	sc = getscreen ()
	sc.onclick (callback)
	
	
def get_etat ():
	""" Retourne l'état courant 
		
		@return : str 
	"""
	global etat
	return etat

def set_etat (state):
	""" Définit l'état courant 
		
		@state : str = le nouvel état 
		
		@return : None
	"""
	global etat
	
	if state not in etats:
		raise EtatInvalide (state)
	
	etat = state 
	# petits trucs ici pour les transitions 
	# iconsole.separateur ()
	iconsole.clear ()
	
	afficher_aide () # Affiche l'aide du nouvel état 
	
def set_ecran (new, t = False):
	""" Change d'écran sur la fenêtre turtle 
		
		@new : str = le nouvel écran
		@t : int = temps de chargement [opts]
		
		@return : None
	"""
	global ecran 
	if new == "plateau":
		if t != False:
			chargement.run (t, "arc")
		
		if moteur.est_en_partie () == True:
			moteur.reprendre_partie ()
		else:
			affichage.plateau ()
			
	elif new == "regles":
		if t != False:
			chargement.run (t, "cercle")
			
		regles.regles (moteur.get_next_mode ())
	elif new == "scores":
		if t != False:
			chargement.run (t, "ligne")

		affichage.high_score ()
	elif new == "fond":
		if t != False:
			chargement.run (t, "ligne") 
	else:
		raise EcranInvalide
	
	ecran = new

def afficher_aide ():
	""" Affiche l'aide globale ainsi que celle de l'état courant 
		
		@return : None
	"""
	pass

def afficher_couleurs ():
	""" Affiche la liste des couleurs disponibles 
		actuellement si possible, ou 
		future si on n'est pas en cours de partie
		
		@return : None
	"""
	nombre_couleurs = False
	try:
		nombre_couleurs = moteur.get_nombre_couleurs ()
	except moteur.PasEnCoursDePartie:
		nombre_couleurs = moteur.get_nombre_couleurs_next ()
	
	def generateur_liste_couleurs (nbr):
		c = couleurs.liste_couleurs ()[0:nbr] # Prend le bon nombre de couleurs
		
		for i in c:
			color (couleurs.string_to_hexa (i))
			begin_fill ()
			carre (40)
			end_fill ()
			ajouter_bouton (i,40,position ()) # Ajoute un bouton
			yield
		
	aller_a (140,200)
	lignes (3, 50, 50, generateur_liste_couleurs (nombre_couleurs))
	
def send (rep):
	""" Envoie une requête utilisateur au Mastermind
		qui va gérer la redirection et les actions 
		nécessaires
		
		@rep : str = la requête
		
		@return : str = l'état actuel 
	"""
	if rep == "help": # Commande indépendante de l'état courant !
		afficher_aide ()
	elif rep == "regles": # Commande indépendante de l'état courant !
		
		
		set_ecran ("regles", 2)
	elif rep == "clear":
		iconsole.clear ()
	elif rep == "scores": # Commande indépendante de l'état courant !
		
		
		set_ecran ("scores", 1)
		
	elif rep == "fortune":
		try:
			maximum = persistance.get_propriete ("phrases", "max")
			maximum = int (maximum)
			aleatoire = randint (0,maximum - 1)
			
		except persistance.CleInvalide:
			pass
		except persistanec.FichierInvalide:
			pass
		except ValueError:
			pass
		except:
			pass
			
	elif rep == "couleurs":
		afficher_couleurs ()
			
	elif get_etat () == "Humain-Joue":
		humain_joue (rep)
	elif get_etat () == "Menu":
		menu (rep)
	elif get_etat () == "Theme":
		theme (rep)
	elif get_etat () == "Niveau":
		niveau (rep)
	elif get_etat () == "Proposer-Code":
		proposer_code (rep)
	elif get_etat () == "Definir-Code":
		definir_code (rep)
	else:
		raise ErreurFatale
	
	return get_etat ()

def humain_joue (rep):
	""" Une fonction qui permet de faire jouer 
		l'humain quand on est dans l'état 
		« Humain-Joue »
		
		@rep : str = l'évènement à gérer
		
		@return : None
		
		@throw :
			LeProgrammeurEstCon
			ErreurFatale
	"""
	global tableau_tampon
	
	if get_etat () != "Humain-Joue":
		raise LeProgrammeurEstCon
	
	if rep == "abandon": # Abandon de la partie -> retour au menu
		
		set_etat ("Menu")
	elif rep == "score":
		try:
			score = moteur.calcul_score ()
		except moteur.PasEnCoursDePartie:
			raise ErreurFatale
	elif rep == "plateau":
		
		try:
			moteur.reprendre_partie ()
		except moteur.PasEnCoursDePartie:
			raise ErreurFatale
		set_ecran ("plateau")
	elif rep == "historique":
		try:
			h = moteur.get_historique ()
		except moteur.PasEnCoursDePartie:
			raise ErreurFatale
		else:
			def generateur_historique (hist):
				for i in hist:
					# i = [[a,b,c,d], (e,f)]
					coup = i[0]
					resultat = i[1]
					
					sa = ""
					if resultat[0] > 1:
						sa = "s"
					
					sb = ""
					if resultat[1] > 1:
						sb = "s"
					
					string = "{0} rouge{1}, {2} blanche{3}".format (resultat[0],sa,resultat[1],sb)
					
					yield (coup,string) 
					
			afficher_liste ("Historique", generateur_historique (h))
	elif rep == "valider":
		
		if ecran != "plateau":
			set_ecran ("plateau")
		
		try:
			r = moteur.verification_solution ( tableau_tampon )
		except moteur.TableauInvalide as exception:
			pass
		else:
			
			if r == "gagne":
				
				
				nom = "aaa"
				
				try:
					moteur.enregistre_score (nom)
				except moteur.PasEnCoursDePartie:
					raise ErreurFatale
				
				set_etat ("Menu")
			elif r == "perdu":
				
				
				set_etat ("Menu")
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

				tableau_tampon = []
				
				iconsole.separateur ()
				afficher(messaga)
				afficher(messagb)
				
	else:
		gestion_tableau (rep) # Gère l'ajout/suppression dans le tableau
			
def theme (rep):
	""" Fonction qui premet de faire réagir le menu Theme
		
		@rep : str = l'évènement
		
		@reutrn : None
		
		@throw :
			LeProgrammeurEstCon
			persistance.FichierInvalide
			persistance.CleInvalide
			
	"""
	if get_etat () != "Theme":
		raise LeProgrammeurEstCon
	
	if rep == "list":
		def gen_liste_theme ():
			for i in affichage.liste_themes ():
				desc = persistance.get_propriete ("backgrounds", "theme:" + i + ":description")
				yield (i,desc)

		afficher_liste ("Themes",gen_liste_theme ())
	elif rep == "valider":
		pass
		set_etat ("Menu")
	elif rep == "actuel":
		# Ce code peut planter ... mais on ne récupère pas l'exception
		# si cela plante ... il faut que ça remonte, l'erreur est trop 
		# grave ...
		pass
	else:
		try:
			
			affichage.choix_theme (int (rep)) # un truc qui peut facilement planter a cause du int
			
			primitives.raz ()
			path = "Images/Theme" + rep + "/fond.gif"
			primitives.bgpic (path)
			set_ecran ("fond")
		except ValueError:
			pass
		except persistance.CleInvalide:
			pass
		except persistance.FichierInvalide:
			pass

def niveau (rep):
	""" Fonction qui fait réagir le menu Niveau
		
		@rep : str = l'évènement
		
		@return : None
	"""
	if get_etat () != "Niveau":
		raise LeProgrammeurEstCon
	
	if rep == "list":
		afficher (str (moteur.get_liste_modes ()))
	elif rep == "actuel":
		afficher ("Le mode de la prochaine partie est " + moteur.get_next_mode ())
	elif rep == "valider":
		afficher ("Niveau modifié pour la prochaine partie")
		set_etat ("Menu")
	else:
		if rep in (moteur.get_liste_modes ()):
			afficher ("Vous avez sélectionné le niveau : " + rep)
			moteur.set_mode (rep)
			set_ecran ("regles", 3)
		else:
			afficher ("Ce niveau est invalide ...")
	

def gestion_tableau (rep):
	""" Fait réagir une gestion des entrées de 
		tableaux en console, ce n'est pas un état
		mais une suite d'actions possibles
		
		@rep : str = l'entrée utilisateur
		
		@return : None
	"""
	global tableau_tampon
	if rep == "annuler":
		try:
			tableau_tampon = tableau_tampon[:-1] # Retire la dernière valeur ...
		except:
			pass
		else:
			pass
	else:
		try:
			tableau_tampon.append (couleurs.couleur_to_string (rep))
		except couleurs.CouleurInvalide:
			pass
		else:
			pass
	

def definir_code (rep):
	""" Fait réagir la définition de code 
	
		@rep : str = l'évènement
		
		@return : None
	"""
	global tableau_tampon 
	
	if get_etat () != "Definir-Code":
		raise LeProgrammeurEstCon
	
	if rep == "abandon":
		
		tableau_tampon = [] 
		set_etat ("Menu")
	elif rep == "valider":
		
		moteur.nouvelle_partie ()
		try:
			r = moteur.definir_code ( tableau_tampon )
		except moteur.TableauInvalide as exception:
			pass
		else:
			tableau_tampon = []
			set_etat ("Menu")
	else:
		gestion_tableau (rep)

def menu (rep):
	""" Fonction qui permet de faire réagir le menu 
		à des actions 
		
		@rep : str = l'évènement
		
		@return : None
	"""
	if get_etat () != "Menu":
		raise LeProgrammeurEstCon
	
	if rep == "ia-code":
		moteur.nouvelle_partie ()
		
		set_ecran ("plateau", 5)
		ia.choisir_code ()
		
	elif rep == "humain-code":
		set_etat ("Definir-Code")
		afficher_couleurs ()
	elif rep == "humain-joue":
		try:
			mode = moteur.get_mode () 
		except moteur.PasEnCoursDePartie:
			pass
		else:
			set_ecran ("plateau", 5)
			
			set_etat ("Humain-Joue") # Change d'état
			afficher_couleurs ()
	elif rep == "ia-joue":
		try:
			mode = moteur.get_mode ()
		except moteur.PasEnCoursDePartie:
			pass
		else:
			
			# afficher_liste ("Les IAs sont", [("knuth", "Une IA très forte"), ("aleatoire", "Une ia ... mauvaise !"), ("matrice","Une IA moyenne")])
			
			"""ia_mode = ""
			demander_ia = True
			while demander_ia == True:
				ia_mode = demander ("Quelle IA")
				if ia_mode in ["matrice", "aleatoire", "knuth"]:
					demander_ia = False
				else:
					afficher ("Ce mode d'IA est invalide !")
			afficher_couleurs ()"""
			
			ia_mode = "aleatoire" # Il faut changer ça plus tard 
			
			set_ecran ("plateau", 3)
			
			for i in ia.jouer (ia_mode):
				primitives.aller_a (200,-200)
				chargement.animation (3,"cercle",20)
			
			moteur.enregistre_score (ia_mode)
			
	elif rep == "theme":
		set_etat ("Theme")
	elif rep == "niveau":
		set_etat ("Niveau")
	else:
		pass
