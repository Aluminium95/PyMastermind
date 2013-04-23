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

def parcourir_colonne (matrice,m):
	for i in range (0,matrice["n"]):
		yield matrice[(i,m)]

def parcourir_ligne (matrice,n):
	for j in range (0,matrice["m"]):
		yield matrice[(n,j)]

def parcourir_lignes (matrice):
	for i in range (0,matrice["n"]):
		l = []
		for j in range (0,matrice["m"]):
			l.append (matrice[(i,j)])
		yield l

def parcourir_colonnes (matrice):
	for j in range (0, matrice["m"]):
		l = []
		for i in range (0,matrice["n"]):
			l.append (matrice[(i,j)])
		yield l
	
def set (matrice,i,j,val):
	matrice[(i,j)] = val

def get (matrice,i,j):
	return matrice[(i,j)]

def display (matrice,univers):
	
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
