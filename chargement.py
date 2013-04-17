#-*- coding: utf-8 -*-
# 
# Affiche un écran qui fait une barre
# de chargement !

# Nos modules à nous 
import persistance
import couleurs
import primitives 

# Python standard
from random import randint
from time import sleep
from random import choice

def init ():
	""" Initialise le module """
	pass # ne fait rien 

def animation (t,mode = "cercle"):
	""" Fait une animation en partant de la position 
		actuelle du pointeur ...

		@t : int = le nombre de tours
		@mode : str (cercle|arc|ligne) = le mode de chargement

		@return : None
	"""
	x,y = primitives.get_position ()

	liste = ["zinzolin","indigo","vert"]
	
	def generer_couleurs (col,n):
		current_color = col
		for i in xrange (0,n):
			current_color = couleurs.eclaircir (current_color, "11")
			primitives.dot (40, current_color)
			yield

	k = 0
	# speed (0)
	for i in range (t):
		# Définit la couleur de ce tour de boucle 
		current_color = couleurs.string_to_hexa (liste[k % len (liste)])

		if mode == "cercle":
			# Fait un cercle ... mouhaha
			primitives.cercle (6,100,generer_couleurs (current_color,6))
		elif mode == "arc":
			for j in range (0,5):
				current_color = couleurs.eclaircir (current_color, "11")
				primitives.dot (40, current_color) 
				primitives.up ()
				primitives.right (20)
				primitives.forward (50)
			primitives.aller_a (x,y)
			primitives.seth (0)
		else: # mode == "ligne"
			primitives.colonnes (1,30,generer_couleurs (current_color,6))
		k += 1


def run (t,mode = "cercle"):
	""" Fait un chargement d'une durée
		de t secondes ... Un super écran ! 

		@t : int = secondes
		@mode : str (cercle|arc|ligne) = le mode d'affichage de la barre de chargement

		@return : None 
	"""
	primitives.hideturtle ()
	
	# Affiche le fond d'écran approprié
	th = persistance.get_propriete ("backgrounds", "theme:courant")

	primitives.bgpic ("Images/Theme{0}/chargement.gif".format (th))
	
	# Affiche une astuce
	astuce = "Vous pouvez modifier la difficulté dans le menu ..."

	xa = int (persistance.get_propriete ("backgrounds","theme:" +  th + ":x:astuce"))
	ya = int (persistance.get_propriete ("backgrounds","theme:" +  th + ":y:astuce"))

	xc = int (persistance.get_propriete ("backgrounds","theme:" +  th + ":x:chargement"))
	yc = int (persistance.get_propriete ("backgrounds","theme:" + th + ":y:chargement"))
	
	
	primitives.aller_a (xa,ya)
	primitives.texte (astuce,"petit")
	
	primitives.aller_a (xc,yc)
	
	primitives.down ()
	animation (t,mode)
	
	primitives.aller_a (0,0)
	primitives.seth (0)

if __name__ == '__main__':
	# Si on lance le module seul
	persistance.init ()
	couleurs.init ()

	init ()
	run (10,"cercle")
	primitives.raz ()
	run (10,"arc")
	primitives.raz ()
	run (10,"ligne")
