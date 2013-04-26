#!/usr/bin/env python2
#-*- coding: utf-8 -*-

# Module qui fait des matrices !

def make (n,m,func):
	""" Crée une matrice (n,m)
		remplie avec la fonction func

		@n : int = nombre de lignes
		@m : int = nombre de colonnes
		@func : fonction = fonction de remplissage

		@return : matrice
	"""
	matrice = {}
	matrice["n"] = n
	matrice["m"] = m
	for i in range (0,n):
		for j in range (0,m):
			matrice[(i,j)] = func (i,j)
	return matrice

def apply (matrice, func):
	""" Applique une fonction à chaque cellule de la matrice
		
		@func : fonction = (i,j,valeur) -> valeur
		
		@return : None
	"""
	for i in range (0, matrice["n"]):
		for j in range (0, matrice ["m"]):
			matrice[(i,j)] = func (i,j,matrice[(i,j)])

def parcourir_matrice (matrice):
	""" Générateur qui parcours la matrice
	
		@return : generator
	"""
	for i in range (0,matrice["n"]):
		for j in range (0, matrice["m"]):
			yield matrice[(i,j)]

def parcourir_colonne (matrice,m):
	""" Générateur qui parcour une colonne de la matrice
		
		@m : int = la colonne
		
		@return : generator
	"""
	for i in range (0,matrice["n"]):
		yield matrice[(i,m)]

def parcourir_ligne (matrice,n):
	""" Générateur qui parcour une ligne de la matrice
		
		@n : int = la ligne
		
		@return : generator
	"""
	for j in range (0,matrice["m"]):
		yield matrice[(n,j)]

def parcourir_lignes (matrice):
	""" Générateur qui parcour les lignes une à une 
		et donne des listes (une par ligne)
		
		@return : generator
	"""
	for i in range (0,matrice["n"]):
		l = []
		for j in range (0,matrice["m"]):
			l.append (matrice[(i,j)])
		yield l

def parcourir_colonnes (matrice):
	""" Générateur qui parcour les colonnes et donne 
		des listes
		
		@return : generator
	"""
	for j in range (0, matrice["m"]):
		l = []
		for i in range (0,matrice["n"]):
			l.append (matrice[(i,j)])
		yield l
	
def set (matrice,i,j,val):
	"""" Définit la valeur dans une case 
		
		@i : int = ligne
		@j : int = colonne
		@v : ? = valeur
		
		@return : None
	"""
	matrice[(i,j)] = val

def get (matrice,i,j):
	""" Retourne la valeur dans une cellule
		
		@i : int = ligne
		@j : int = colonne
		
		@return . ?
	"""
	return matrice[(i,j)]

def display (matrice,univers):
	""" Une fonction qui affiche une matrice 
		à l'écran ... sans utiliser iconsole ?!
		
		@univers : [str ...] = nom des colonnes 
		
		@return : None
	"""
	print (" |" + "|".join (univers))
	
	tailles = [len (k) for k in univers]

	k = 0
	for i in parcourir_lignes (matrice):
		s = str (k)
		for p,j in enumerate (i):
			s += "|" + " " * (tailles[p] - len (str (j))) + str (j)
		s += "|"
		print (s)
		k += 1
	print ("\n")
