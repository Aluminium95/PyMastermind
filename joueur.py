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

import primitives 
import chargement
from random import randint 

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

# C'est un gros paquet d'aide !
aide = {
	"global" : {
		"quit" : "Quitte le programme ...",
		"regles" : "Affiche les règles du jeu ...",
		"scores" : "Affiche les meilleurs scores du jeu ...",
		"fortune" : "Affiche une petite phrase aléatoire sympa ...",
		"couleurs" : "Affiche la liste des couleurs disponibles",
		"clear" : "Efface l'écran de la console ..."
	},
	"Menu" : {
		"ia-code" : "Fait décider un code à trouver par une IA",
		"humain-code" : "Fait rentrer un code à l'utilisateur",
		"theme" : "Permet à l'utilisateur de chosir un thème",
		"niveau" : "Permet à l'utilisateur de changer de niveau de difficulté"
	},
	"Menu-Partie" : {
		"ia-joue" : "Fait trouver le code par une IA (nécessite qu'un code ai été défini avant)",
		"humain-joue" : "Fait trouver le code à l'utilisateur",
		"abandon" : "Revient au menu principal"
	},
	"Niveau" : {
		"list" : "Fait la liste des niveaux disponibles",
		"actuel" : "Affiche le niveau actuel de difficulté",
		"valider" : "Enregistre le niveau sélectionné et revient au menu",
		"@" : "Une autre chaine de caractère est prise comme un niveau"
	},
	"Theme" : {
		"list" : "Fait la liste des thèmes disponibles",
		"actuel" : "Affiche le thème actuel ...",
		"valider" : "Engeristre le thème sélectionné et revient au menu",
		"@" : "Sélectionne le texte rentré comme un thème"
	},
	"Humain-Joue" : {
		"plateau" : "Permet de réafficher le plateau de jeu",
		"score" : "Permet de savoir le score actuel",
		"abandon" : "Permet de revenir au menu, et abandonner la partie",
		"historique" : "Permet d'afficher l'historique des coups déjà joués et leur réponses",
		"valider" : "Propose le tableau au mastermind et affiche la réponse, revient à l'état « Humain-Joue »",
		"annuler" : "Supprime le dernier item du tableau",
		"historique" : "Permet d'afficher l'historique des coups déjà joués et leur réponses",
		"recommencer" : "Permet de vider le tableau, pour recommencer un coup à zéro",
		"@" : "Une autre chaine est prise comme une couleur à ajouter en fin de tableau"
	},
	"Definir-Code" : {
		"abandon" : "Revient au menu en annulant la partie actuelle",
		"valider" : "Valide le code et revient au menu, la partie est lancée !",
		"annuler" : "Supprime du tableau la dernière entrée",
		"recommencer" : "Vide le tableau pour recommencer un nouveau code",
		"@" : "Une autre chaine de caractères est prise comme une couleur à ajouter à la fin"
	}
}


etats = ["Menu","Menu-Partie","Humain-Joue","Theme","Niveau","Proposer-Code","Definir-Code"]
ecrans = ["plateau", "regles", "scores"]
etat = ""
ecran = "plateau" # Quel est l'écran actuel ?
tableau_tampon = []

def init ():
	""" Constructeur 
		
		@initial : str = l'état de départ 
		
		@return : Mastermind 
	"""
	set_etat ("Menu")

def afficher (quelquechose, t = 0):
	""" Une surcouche de iconsole.afficher 
		qui met automatiquement l'état courant 
		en « acteur »
		
		@quelquechose : str = un truc à afficher 
		@t : int = nombre de tabulations [opts]
		
		@return : None
	"""
	iconsole.afficher (get_etat (), quelquechose, t)

def afficher_liste (quelquechose, generateur, t = 0):
	""" Encore une surcouche qui englobe iconsole.afficher_liste
		
		@quelquechose : str = texte
		@generateur : generator = générateur de liste
		@t : int = tabulations [opts]
		
		@return : None
	"""
	iconsole.afficher_liste (get_etat (), quelquechose, generateur, t)

def demander (quelquechose, t = 0):
	""" Une surcouche de iconsole.demander 
		qui met l'état actuel en « acteur »
		
		@quelquechose : str = un truc à afficher 
		@t : int = nombre de tabulations [opts]
		
		@return : str
	"""
	return iconsole.demander (get_etat (), quelquechose, t)
	
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
	afficher ("Vous êtes maintenant dans un nouveau mode")
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
	# On Crée un générateur de l'aide actuelle
	# pour personnaliser un peu l'affichage de la liste 
	def gen_help ():
		yield "Commandes globales ..."
		for i,j in aide["global"].items ():
			yield ("\t" + i,j)
		
		yield "Commandes du mode " + get_etat ()
		for i,j in aide[get_etat ()].items ():
			yield ("\t" + i,j)
	# On l'affiche avec le magnifique module iconsole
	afficher_liste ("Aide : ", gen_help ())

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
		afficher ("Vous n'êtes pas en cours de partie, on affiche les couleurs futurement disponibles")
		nombre_couleurs = moteur.get_nombre_couleurs_next ()
	
	def generateur_liste_couleurs (nbr):
		abvrs = couleurs.liste_abreviations ()
		for i in abvrs[0:nbr]:
			a = "({0}) {1}".format (i, couleurs.abrv_to_string (i))
			yield a
		
	afficher_liste ("Couleurs futurement disponibles",generateur_liste_couleurs (nombre_couleurs))

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
		afficher ( "Affichage des règles sur la fenêtre graphique ...")
		
		set_ecran ("regles", 2)
	elif rep == "clear":
		iconsole.clear ()
	elif rep == "scores": # Commande indépendante de l'état courant !
		afficher ("Affichage des scores sur la fenêtre graphique ...")
		
		set_ecran ("scores", 1)
		
	elif rep == "fortune":
		try:
			maximum = persistance.get_propriete ("phrases", "max")
			maximum = int (maximum)
			aleatoire = randint (0,maximum - 1)
			afficher (persistance.get_propriete ("phrases", str (aleatoire)))
		except persistance.CleInvalide:
			afficher ( "Il est impossible de récupérer la fortune ... le fichier « phrases » doit être corrompu »")
		except persistanec.FichierInvalide:
			afficher ( "Le fichier est introuvable ... Cela implique un problème dans le CODE SOURCE ... revenez plus tard ...")
		except ValueError:
			afficher ( "La valeur de « max » dans « phrases » est fausse et ne représente pas un nombre valide ...")
		except:
			afficher ( "Une erreur inconnue est survenue ... ")
			
	elif rep == "couleurs":
		afficher_couleurs ()
			
	elif get_etat () == "Humain-Joue":
		humain_joue (rep)
	elif get_etat () == "Menu":
		menu (rep)
	elif get_etat () == "Menu-Partie":
		menu_partie (rep)
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
		afficher ("Vous avez abandonné la partie ...")
		set_etat ("Menu")
	elif rep == "score":
		try:
			afficher (moteur.calcul_score ())
		except moteur.PasEnCoursDePartie:
			raise ErreurFatale
	elif rep == "plateau":
		afficher ("Le plateau est affiché, vous pouvez proposer des solutions")
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
		afficher ("Valide le nouveau code ...")
		if ecran != "plateau":
			set_ecran ("plateau")
		
		try:
			r = moteur.verification_solution ( tableau_tampon )
		except moteur.TableauInvalide as exception:
			afficher ("Le tableau est invalide : {0}".format (exception.message))
		else:
			
			if r == "gagne":
				afficher ("Vous avez gagné !!!")
				
				nom = demander ("Nom du joueur")
				
				try:
					moteur.enregistre_score (nom)
				except moteur.PasEnCoursDePartie:
					raise ErreurFatale
				
				set_etat ("Menu")
			elif r == "perdu":
				afficher ("Vous avez perdu !!!")
				
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
		afficher ("Theme modifié ... ")
		set_etat ("Menu")
	elif rep == "actuel":
		# Ce code peut planter ... mais on ne récupère pas l'exception
		# si cela plante ... il faut que ça remonte, l'erreur est trop 
		# grave ...
		afficher ("Le theme actuel est le numero {0}".format (persistance.get_propriete ("backgrounds","theme:actuel")))
	else:
		try:
			
			affichage.choix_theme (int (rep)) # un truc qui peut facilement planter a cause du int
			afficher ("Selection theme : " + rep)
			primitives.raz ()
			path = "Images/Theme" + rep + "/fond.gif"
			primitives.bgpic (path)
			set_ecran ("fond")
		except ValueError:
			afficher ("Il faut entrer le numéro du thème ...")
		except persistance.CleInvalide:
			afficher ("Euh ... ce thème ne peut être chargé ...")
		except persistance.FichierInvalide:
			afficher ("Priez pauvres fous, le fichier de configuration est introuvable !")

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
			afficher ("Plus rien à annuler ...")
		else:
			afficher (tableau_tampon)
	elif rep == "recommencer":
		tableau_tampon = [] # Vide le tableau
		afficher (tableau_tampon)
	else:
		try:
			tableau_tampon.append (couleurs.couleur_to_string (rep))
		except couleurs.CouleurInvalide:
			afficher ("Cette couleur n'existe pas ...")
		else:
			afficher (tableau_tampon)
	

def definir_code (rep):
	""" Fait réagir la définition de code 
	
		@rep : str = l'évènement
		
		@return : None
	"""
	global tableau_tampon 
	
	if get_etat () != "Definir-Code":
		raise LeProgrammeurEstCon
	
	if rep == "abandon":
		afficher ("Annule la propositon de code ... ")
		tableau_tampon = [] 
		set_etat ("Menu")
	elif rep == "valider":
		afficher ("Valide le nouveau code ...")
		moteur.nouvelle_partie ()
		try:
			r = moteur.definir_code ( tableau_tampon )
		except moteur.TableauInvalide as exception:
			afficher ("Le tableau est invalide : {0}".format (exception.message))
		else:
			tableau_tampon = []
			set_etat ("Menu-Partie")
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
		afficher ( "L'IA va choisir un code, on commence une nouvelle partie")
		set_ecran ("plateau", 5)
		ia.choisir_code ()
		afficher ( "L'IA a déterminé un code")
		set_etat ("Menu-Partie")
	elif rep == "humain-code":
		set_etat ("Definir-Code")
		afficher_couleurs ()
	
	elif rep == "theme":
		set_etat ("Theme")
	elif rep == "niveau":
		set_etat ("Niveau")
	else:
		afficher ("Cette requête est invalide dans le menu ...")		
			
def menu_partie (rep):
	
	if rep == "humain-joue":
		try:
			afficher ("Le niveau actuel est : " + moteur.get_mode ())
		except moteur.PasEnCoursDePartie:
			afficher ("Mmmh ... vous n'êtes pas en cours de partie ... il faut définir un code !")
		else:
			set_ecran ("plateau", 5)
			
			set_etat ("Humain-Joue") # Change d'état
			afficher_couleurs ()
	elif rep == "abandon":
		set_etat ("Menu")
	elif rep == "ia-joue":
		afficher ("L'IA va jouer une partie")
		try:
			afficher ("Le niveau actuel est : " + moteur.get_mode ())
		except moteur.PasEnCoursDePartie:
			afficher ("Vous n'êtes pas en cours de partie ... il faut définir un code !")
		else:
			afficher_liste ("Les IAs sont", [("knuth", "Une IA très forte"), ("aleatoire", "Une ia ... mauvaise !"), ("matrice","Une IA moyenne")])
			
			ia_mode = ""
			demander_ia = True
			while demander_ia == True:
				ia_mode = demander ("Quelle IA")
				if ia_mode in ["matrice", "aleatoire", "knuth"]:
					demander_ia = False
				else:
					afficher ("Ce mode d'IA est invalide !")
			afficher_couleurs ()
			
			set_ecran ("plateau", 3)
			
			for i in ia.jouer (ia_mode):
				primitives.aller_a (200,-200)
				chargement.animation (3,"cercle",20)
			
			moteur.enregistre_score (ia_mode)
	else:
		afficher ("La requête n'est pas valide dans Menu-Partie ...")
	
	
