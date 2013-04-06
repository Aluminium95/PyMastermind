#-*- coding: utf-8 -*-
# Module interface graphique

import affichage
import moteur 
import fsm


def init ():
	# some initialisation here

def to_menu ():
	affichage.afficher_menu ()


def to_choix_code ():
	affichage.afficher_blabla ()


def to_jeu ():
	affichage.clean ()

def run ():
	# Création d'une machine :-)
	machine = fsm.new ()

	# Exemple de transitions ... 
	fsm.set_transition (machine, "menu", "choix-code", to_choix_code)
	fsm.set_transition (machine, "choix-code", "menu", to_menu)
	fsm.set_transition (machine, "choix-code", "jeu", to_jeu)
	fsm.set_transition (machine, "jeu", "menu", to_menu)

	
	# while bla bla bla 


