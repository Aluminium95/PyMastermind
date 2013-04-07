#-*- coding: utf-8 -*-
# Module interface graphique

import affichage
import moteur 
import fsm

from turtle import *

machine = False

def to_menu (m):
	print "to menu"

def to_choix_code (m):
	print "to choix code"

def to_jeu (m):
	print "to jeu"


def init ():
	global machine 
	
	# Création d'une machine :-)
	machine = fsm.new ()

	# Exemple de transitions ... 
	fsm.set_transition (machine, "menu", "choix-code", to_choix_code)
	fsm.set_transition (machine, "choix-code", "menu", to_menu)
	fsm.set_transition (machine, "choix-code", "jeu", to_jeu)
	fsm.set_transition (machine, "jeu", "menu", to_menu)

	fsm.transition (machine, 'menu')

def dispatcher (x,y):
	""" Fonction qui récupère les clics turtle 
		et les dispatche sur les boutons correspondants 
		
		@x : int = position x du curseur
		@y : int = position y du curseur

		@return : None
	"""
	global machine 
	
	print x,y
	
	st = fsm.get_state (machine) # État courant 
	if st == 'menu':
		fsm.transition (machine, 'choix-code')
	elif st == 'choix-code':
		fsm.transition (machine, 'jeu')
	elif st == 'jeu':
		fsm.transition (machine, 'menu')

def run ():

	sc = getscreen ()
	# On crée une fonction anonyme, qui permet de « capturer » la variable machine 
	# et la donner en argument à dispatcher 
	sc.onclick (dispatcher)
	# Boucle indéfiniment !
	mainloop ()

if __name__ == '__main__':
	init ()
	run ()
