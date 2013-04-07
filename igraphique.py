#-*- coding: utf-8 -*-
# Module interface graphique

import affichage
import moteur 
import fsm

from turtle import *

# Boutons sous la forme 
#
# [nom, x, y, l, c, t]
#
# @nom : le nom 
# @(x,y) : la position 
# l : taille du côté du carré 
# c : couleur du carré 
# t : le texte à afficher 



# La machine est par défaut : False
machine = False

boutons_menu = []
boutons_couleurs = []
boutons_difficulte = []

# Un pointeur vers les boutons actuels 
boutons_actuels = boutons_menu

def to_menu (m):
	affichage.reset ()
	boutons_actuels = boutons_menu
	afficher_boutons (boutons_actuels)
	print "to menu"

def to_choix_code (m):
	affichage.reset ()
	boutons_actuels = boutons_couleurs
	afficher_boutons (boutons_actuels)
	print "to choix code"

def to_jeu (m):
	affichage.reset ()
	boutons_actuels = boutons_couleurs
	afficher_boutons (boutons_actuels)
	print "to jeu"


def init ():
	global machine 
	
	# Création d'une machine :-)
	machine = fsm.new ()

	# Définition des états 
	states = ["menu", "choix-code", "jeu", "regles", "choix-difficulte", "fin"]
	for i in states:
		fsm.add_state (machine, i)

	# Exemple de transitions ... 
	fsm.set_transition (machine, "menu", "choix-code", to_choix_code)
	fsm.set_transition (machine, "choix-code", "menu", to_menu)
	fsm.set_transition (machine, "choix-code", "jeu", to_jeu)
	fsm.set_transition (machine, "jeu", "menu", to_menu)

	fsm.transition (machine, 'menu')

	# Génération des boutons correspondant 
	# aux différents états ..
	quitter = ["quitter", 120,245, 50, "red", "quitter"]
	boutons_menu.append (quitter)
	boutons_couleurs.append (quitter)
	boutons_difficulte.append (quitter)
	

def afficher_boutons (tableau):
	""" Affiche la liste de boutons passé en argument
		
		@tableau : list of boutons = la liste de boutons
			bouton : [nom, x, y, l, couleur, texte]
		@return : None
	"""
	for i in tableau:
		affichage.creer_bouton (i[1],i[2],i[3],i[4],i[5])

def get_button (x,y):
	""" Retourne le bouton sur lequel le clic 
		aux coordonnées (x,y) porte

		@x : int = coordonnée x
		@y : int = coordonnée y

		@return : string (button name) | False
	"""
	# On regarde dans les boutons actifs 
	# s'il y en a un qui correspond
	for b in boutons_actuels:
		if b[1] < x < b[1] + b[3] and b[2] < y < b[2] + b[3]:
			return b[0]
	return False

def dispatcher (x,y):
	""" Fonction qui récupère les clics turtle 
		et les dispatche sur les boutons correspondants 
		
		@x : int = position x du curseur
		@y : int = position y du curseur

		@return : None
	"""
	global machine 
	
	st = fsm.get_state (machine) # État courant 
	
	# On récupère le bouton sur lequel on a cliqué 
	bt = get_button (x,y)
	
	# ICI se trouve le gros switch !!!!
	# C'est là que se trouve TOUT le gros du code 
	# Il faut NÉCESSAIREMENT comprendre ce qui se passe ici
	if bt == "quitter": # on quitte 
		print "On se casseeeeeeee"
	
	# Les autres évènements dépendent 
	# de l'état dans lequel on est ...
	if st == 'menu': # Menu a des boutons différents
		fsm.transition (machine, 'choix-code')
	elif st == 'choix-code' or st == 'jeu': # là, les boutons sont les mêmes !

		fsm.transition (machine, 'jeu')
	elif st == 'choix-difficulte': # boutons différents 
		fsm.transition (machine, 'menu')

def run ():
	affichage.init ()

	sc = getscreen ()
	# On crée une fonction anonyme, qui permet de « capturer » la variable machine 
	# et la donner en argument à dispatcher 
	sc.onclick (dispatcher)
	
	# On affiche les boutons 
	afficher_boutons (boutons_actuels)
	
	# Boucle indéfiniment !
	mainloop ()

if __name__ == '__main__':
	init ()
	run ()
