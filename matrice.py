#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Module qui fait des matrices !
# Pas d'addition, soustraction ...
# Juste des tableaux à deux dimensions
# que l'on peut parcourir

# DEB EXCEPTIONS

class DimensionsInvalides (Exception):
	pass

# FIN EXCEPTIONS

def make (n,m,func):
	""" Crée une matrice (n,m)
		remplie avec la fonction func

		@n : int = nombre de lignes
		@m : int = nombre de colonnes
		@func : fonction = fonction de remplissage

		@return : matrice
	"""
	matrice = {}
	matrice["lignes"] = n # Le nombre de lignes
	matrice["cols"] = m # le nombre de colonnes
	for i in range (0,n):
		for j in range (0,m):
			matrice[(i,j)] = func (i,j)
	return matrice

def apply (matrice, func):
	""" Applique une fonction à chaque cellule de la matrice
		
		@func : fonction = (i,j,valeur) -> valeur
		
		@return : None
	"""
	for i in range (0, matrice["lignes"]):
		for j in range (0, matrice ["cols"]):
			matrice[(i,j)] = func (i,j,matrice[(i,j)])

def add (f,m1,m2):
	""" Fait la somme de deux matrices 
		
		@f  : fonction = fonction qui fait la somme
		@m1 : matrice = matrice une
		@m2 : matrice = matrice deux

		@return : matrice = la somme 
		
		@throw : DimensionsInvalides
	"""
	if m1["lignes"] != m2["lignes"] or m1["cols"] != m2["cols"]:
		raise DimensionsInvalides
	
	def remplissage (i,j):
		return f (get (m1,i,j) ,get (m2,i,j))

	return make (m1["lignes"],m1["cols"],remplissage) # Crée une nouvelle matrice 

def mul (f1,f2,m1,m2):
	""" Fait la multiplication de deux matrices
		
		@f1 : fonciton = fonction qui multiplie
		@f2 : fonction = fonction qui fait la somme 
		@m1 : matrice  = matrice une
		@m2 : matrice = matrice deux

		@return : matrice = la matrice produit

		@throw : DimensionsInvalides
	"""
	
	if m1["cols"] != m2["lignes"]:
		raise DimensionsInvalides

	def remplissage (i,j):
		ligne = list (parcourir_ligne (m1,i))
		col   = list (parcourir_colonne (m2,j))
		
		r = utils.bi_map (f1,ligne,col) # On fait la multiplication deux a deux

		return utils.foldl (f2,r[0],r[1:]) # On fait la somme 
	
	return make (m1["lignes"],m2["cols"], remplissage)

def parcourir_matrice (matrice):
	""" Générateur qui parcours la matrice
	
		@return : generator
	"""
	for i in range (0,matrice["lignes"]):
		for j in range (0, matrice["cols"]):
			yield matrice[(i,j)]

def parcourir_colonne (matrice,m):
	""" Générateur qui parcour une colonne de la matrice
		
		@m : int = la colonne
		
		@return : generator
	"""
	for i in range (0,matrice["lignes"]):
		yield matrice[(i,m)]

def parcourir_ligne (matrice,n):
	""" Générateur qui parcour une ligne de la matrice
		
		@n : int = la ligne
		
		@return : generator
	"""
	for j in range (0,matrice["cols"]):
		yield matrice[(n,j)]

def parcourir_lignes (matrice):
	""" Générateur qui parcour les lignes une à une 
		et donne des listes (une par ligne)
		
		@return : generator
	"""
	for i in range (0,matrice["lignes"]):
		l = []
		for j in range (0,matrice["cols"]):
			l.append (matrice[(i,j)])
		yield l

def parcourir_colonnes (matrice):
	""" Générateur qui parcour les colonnes et donne 
		des listes
		
		@return : generator
	"""
	for j in range (0, matrice["cols"]):
		l = []
		for i in range (0,matrice["lignes"]):
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
	print (" |" + "|".join (univers))  # Noms des colonnes
	
	tailles = [len (k) for k in univers] # Taille des colonnes 

	k = 1 # Numéro de ligne
	for i in parcourir_lignes (matrice):
		s = str (k)
		for p,j in enumerate (i):
			s += "|" + " " * (tailles[p] - len (str (j))) + str (j)
		s += "|"
		print (s)
		k += 1
	print ("\n")
