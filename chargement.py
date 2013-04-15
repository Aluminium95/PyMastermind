#-*- coding: utf-8 -*-
# 
# Affiche un écran qui fait une barre
# de chargement !

from time import sleep

import persistance
from turtle import * 
from random import randint
from random import choice
import couleurs

def init ():
	""" Initialise le module """
	print "initialisation"

def polygone (n,w,c):
	up ()
	
	color (c)
	begin_fill ()
	
	for i in range (0,n):
		forward (w)
		right (360 / n)

	end_fill ()
	up ()

def run (t,mode = "cercle"):
	""" Fait un chargement d'une durée
		de t secondes ... Un super écran ! 

		@t : int = secondes
		@mode : str (cercle|arc|ligne) = le mode d'affichage de la barre de chargement

		@return : None 
	"""
	# Affiche le fond d'écran approprié
	th = persistance.get_propriete ("backgrounds", "theme:courant")

	bgpic ("Images/Theme{0}/chargement.gif".format (th))
	
	# Affiche une astuce
	astuce = "Vous pouvez modifier la difficulté dans le menu ..."

	xa = int (persistance.get_propriete ("backgrounds","theme:" +  th + ":x:astuce"))
	ya = int (persistance.get_propriete ("backgrounds","theme:" +  th + ":y:astuce"))

	xc = int (persistance.get_propriete ("backgrounds","theme:" +  th + ":x:chargement"))
	yc = int (persistance.get_propriete ("backgrounds","theme:" + th + ":y:chargement"))
	
	
	up ()
	goto (xa,ya)
	write (astuce,False,"left", ("calibri",12,"normal"))
	
	up ()
	goto (xc,yc)
	down ()
	
	# liste = couleurs.liste_couleurs ()[0:8]
	# Configuration spéciale violet !
	liste = ["zinzolin", "indigo"]
	k = 0
	# speed (0)
	for i in range (t):
		# Définit la couleur de ce tour de boucle 
		current_color = couleurs.string_to_hexa (liste[k % len (liste)])

		if mode == "cercle":
			for j in range (0,6): # On fait 6 trucs
				#polygone (4,50,couleurs.string_to_hexa (c))
				current_color = couleurs.eclaircir (current_color, "11")
				dot (40, current_color)
				up ()
				right (360 / 6)
				forward (70)
		elif mode == "arc":
			for j in range (0,5):
				# polygone (4,40, couleurs.string_to_hexa (liste[k % len (liste)]))
				current_color = couleurs.eclaircir (current_color, "11")
				dot (40, current_color) 
				up ()
				right (20)
				forward (50)
			up ()
			goto (xc,yc)
			seth (0)
		else: # mode == "ligne"
			for j in range (0,5):
				# polygone (4, 40, couleurs.string_to_hexa (liste[k % len (liste)]))
				current_color = couleurs.eclaircir (current_color, "11")
				dot (30, current_color)
				up ()
				forward (40)
			up ()
			goto (xc,yc)
		k += 1
	goto (0,0)
	seth (0)
if __name__ == '__main__':
	# Si on lance le module seul
	persistance.init ()
	couleurs.init ()

	init ()
	hideturtle ()
	run (10,"cercle")
	clear ()
	run (10,"arc")
	clear ()
	run (10,"ligne")
