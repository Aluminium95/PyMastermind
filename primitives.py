#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Module qui permet 
# de faire abstraction de 
# turtle (un peu)
# et qui met à disposition des 
# primitives de dessin plus 
# possées !


# Le module expose de plus toutes les fonctions 
# De TURTLE !!!
from turtle import * 

# EXCEPTIONS

class ModeTexteInvalide (Exception):
	pass

# FIN EXCEPTIONS

def init ():
	""" Initialise le module 
		
		@return : None
	"""
	pass

def get_position ():
	""" Retourne la position du pointeur 
		
		@return : (x,y) position du pointeur
	"""
	return position ()

def aller_a (x,y,trace = False):
	""" Se déplace aux coordonnées x,y
		
		@x : int = position en x
		@y : int = position en y
		@trace : bool = si on trace le trait

		@return : None
	"""

	if trace == False:
		up ()
	goto (x,y)

def polygone (n,w,c = False):
	""" Crée un polygone régulier de n côtés de longueur w
		et de couleur c
		
		Le polygone est crée en partant du point actuel 
		de turtle, et se construit en allant vers la droite
		
		@n : int = le nombre de côtés 
		@w : int = la taille d'un côté
		@c : color = une couleur (type turtle)
		
		@return : None
		
		@avance : le pointeur revient à sa position initiale, dans sa 
			direction initiale !
	"""
	if c != False:
		color (c)
		
	down ()
	for i in range (0,n):
		forward (w - 1) # On prend en compte la taille du trait qui fait déjà 1px
		left (360 / n)
	up ()
	
def carre (w,c = False):
	""" Crée un carré de longueur w et de couleur c
	
		Le carré est crée à partir du point actuel de turtle 
		en allant vers la gauche.
		
		@w : int = la taille du côté
		@c : TurtleColor = la couleur du carré
		
		@return : None
		
		@avance : le pointeur revient à sa position initiale, dans 
			sa direction initiale 
	"""
	polygone (4, w, c)
	
def rectangle (w,l, c = False):
	""" Crée un recangle de largeur w de longueur l et 
		de couleur c (si définie)
		
		Le rectangle se fait en allant vers la Gauche
		
		@w : int = largeur
		@l : int = longueur
		@c : TurtleColor = la couleur du carré 
		
		@return : None
		
		@avance : le pointeur revient à la position initiale avec sa 
			direction initiale
	"""
	if c != False:
		color (c)
	
	down ()
	for i in range (0,4):
		if i % 2 == 0:
			forward (w - 1)
		else:
			forward (l - 1)
		left (90)
	up ()
		
	
def texte (text, t = "normal"):
	""" Écrit du texte sur l'écran, de manière jolie ...
		
		@text : str = le texte à écrire
			avec le pointeur comme repère bas-gauche de la première lettre
		@t : str (normal | important | petit) = le type de texte
		
		@return : None | False (si le @t est mauvais)
		
		@avance : le pointeur revient à sa position initiale, dans sa
			direction initiale !
	"""
	
	if t == "normal":
		write (text, False, "left", ("calibri",16,"normal"))
	elif t == "important":
		write (text, False, "left", ("calibri",20,"underline"))
	elif t == "petit":
		write (text, False, "left", ("calibri",12,"normal"))
	else:
		raise ModeTexteInvalide
		
def colonnes (n,c,l,generateur):
	""" Crée des colonnes de n lignes, appelant 
		périodiquement la fonction func
		
		@n : int = nombre de lignes 
		@c : int = espace entre les lignes
		@l : int = espace entre les colonnes 
		@generateur: generator = un générateur python
		
		@return : None
		
		@avance : le pointeur ne bouge pas !
			- à chaque dessin, le pointeur conserve l'angle 
				laissé par le précédent dessin !
	"""
	
	x,y = position () # Récupère la position initiale de turtle 
	a = heading () # Récupère l'angle absolu de la tortue 
	
	k = 0 # Nombre d'éléments actuels dans la colonne 
	p = 0 # Numéro de la colonne actuelle  
	
	for i in generateur:
		k += 1
		if k == n:
			k = 0
			p += 1
		
		# on se place sur la bonne ligne, bonne colonne
		aller_a (x + p * l, y - k * c, False)

	seth (a)
	aller_a (x,y, False)

def lignes (n,l,c,generateur):
	""" Crée une ligne de n élément, espacés par l pxiels
		et revient à la ligne avec un interligne de c pixels
		en utilisant le générateur pour les remplir

		@n : int = nombre d'éléments par ligne
		@l : int = espace entre deux éléments
		@c : int = espace entre deux lignes
		@generateur : generator = generateur

		@return : None
	"""
	a = heading ()
	x,y = position ()
	
	k = 0 # La ligne actuelle
	p = 0 # La colonne actuelle

	for i in generateur:
		p += 1
		if p == n:
			p = 0
			k += 1
		aller_a (x + p * l, y - k * c, False)

	seth (a)
	aller_a (x,y, False)
	
def arc (an,dist, generateur):
	""" Crée un arc de cercle avec chaque point 
		espacés de dist et avec un angle relatif de an

		@an : int = l'angle relatif de décalage entre deux points
		@dist : int = la distance entre deux points
		@generateur : generator = la fonction génératrice

		@return : None

		@avance : Le pointeur est remis à sa place initiale après 
			utilisation, et dans son orientation initiale

	"""
	x,y = position ()
	a = heading ()

	for i in generateur:
		right (an)
		up ()
		fd (dist)
	
	seth (a)
	aller_a (x,y, False)

def cercle (npts, distance, generateur):
	""" Crée un cercle avec n points, appelant la fonction 
		pour chaque point, le cercle a un rayon de distance
		et est de centre la position du pointeur 

		@npts : int = nombre de points 
			le premier point est vers le nord !
		@distance : int = rayon du cercle
		@generateur : generator = fonction génératrice 

		@return : None

		@avance : garde l'angle et la position du pointeur avant 
			l'opération !
	"""
	# Sauvegarde les coordonnées :-)
	x,y = position ()
	a = heading ()

	angle = 90
	seth (angle)
	up ()
	forward (distance)
	down ()
	

	for i in generateur:
		aller_a (x,y,False)
		angle = angle - 360.0 / npts
		seth (angle)
		up ()
		forward (distance)
		down ()
	
	seth (a)
	aller_a (x,y)

def raz ():
	""" Remise À Zéro de l'écran : pointeur réinitialisé (orientation et position) 
		et efface tout ce qu'il y avait, y compris le fond
			
		@return : None
	"""
	reset () # Réinitialise tout (position,angle etc ...)
	clear () # Efface l'écran
	bgpic ("") # Efface le fond d'écran
	hideturtle () # Cache la tortue
	speed (0) # On va très vite !
	up () # On lève le crayon
