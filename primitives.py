# -*- coding: utf-8 -*-
#
# Module qui permet 
# de faire abstraction de 
# turtle (un peu)
# et qui met à disposition des 
# primitives de dessin plus 
# possées !

from turtle import * 


def polygone (n,w,c):
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
	color (c)
	down ()
	for i in range (0,n):
		forward (w)
		right (360 / n)
	up ()
	
def carre (w,c):
	""" Crée un carré de longueur w et de couleur c
	
		Le carré est crée à partir du point actuel de turtle 
		en allant vers la droite.
		
		@w : int = la taille du côté
		@c : int = la couleur du carré
		
		@return : None
		
		@avance : le pointeur revient à sa position initiale, dans 
			sa direction initiale 
	"""
	polygone (4, w, c)
	
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
		return False
		
def colonnes (n,c,l,func):
	""" Crée des colonnes de n lignes, appelant 
		périodiquement la fonction func
		
		@n : int = nombre de lignes 
		@c : int = espace entre les lignes
		@l : int = espace entre les colonnes 
		@func : generator = une fonction génératrice
		
		@return : None
		
		@avance : le pointeur est déplacé, mais garde son orientation !
	"""
	
	x,y = position () # Récupère la position initiale de turtle 
	a = heading () # Récupère l'angle absolu de la tortue 
	
	k = 0 # Nombre d'éléments actuels dans la colonne 
	p = 1 # Numéro de la colonne actuelle  
	
	for i in func ():
		k += 1
		if k == n:
			k = 0
			up ()
			goto (x + p * l,y)
			seth (a)
			p += 1
		seth (0)
		right (90)
		fd (c)
		seth (a)

