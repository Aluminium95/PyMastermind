#!/usr/bin/env python
#-*- coding: utf-8 -*-

# themes.py
#
# Ce module sert à fédérer la gestion 
# des thèmes au travers du programme,
# il permet de sélectionner le thème 
# courant, de trouver les thèmes,
# de faire des listes, des tris 
# tout ce que l'on veut avec des thèmes !

import persistance

# DEB EXCEPTIONS

class ThemeCorrompu (Exception):
	def __init__ (self,theme):
		self.theme = theme

# FIN EXCEPTIONS

def actuel ():
	""" Retourne le thème actuel """
	return persistance.get_propriete ("backgrounds", "theme:courant")

def maximum ():
	""" Retourne le thème maximal """
	try:
		max_theme = persistance.get_propriete ("backgrounds","theme:max")
	except persistance.CleInvalide:
		pass
	except persistance.FichierInvalide:
		pass
	else:
		try:
			return int (max_theme)
		except ValueError:
			raise persistance.ValeurInvalide ("backgrounds","theme:max")

def choix_theme (nbr_theme = 1):
	""" Sélectionne un thème (modifie le fichier de configuration)
		
		@nbr_theme : int = le numéro du nouveau thème sélectionné
		
		@return : None
		
		@throw :
			persistance.CleInvalide
			persistance.FichierInvalide
			ValueEror # si jamais il y a une valeur erronée dans backgrounds -> theme:max
	"""
	if not isinstance (nbr_theme, int):
		nbr_theme = 1
	
	max_theme = persistance.get_propriete ("backgrounds","theme:max")
	
	if nbr_theme > int (max_theme):
		nbr_theme = 1
	
	persistance.set_propriete ("backgrounds","theme:courant",str (nbr_theme))

def get_theme_opts (t,*args):
	l = []
	for j in args:
		try:
			s = "theme:{0}:{1}".format (t,j)
			l.append (persistance.get_propriete ("backgrounds",s))
		except:
			pass # RàF
	return l

def parcourir_themes_opts (*args):
	""" Crée la liste des thèmes avec 
		des options intéressantes 
	"""
	for i in range (1,maximum () + 1):
		yield get_theme_opts (i,*args) # *args -> ré-expand 
		
def liste_themes_opts (*args):
	return list (parcourir_themes_opts (*args))
		
def liste_themes ():
	# C'est con ... ça génère ["1", "2", ..., "max"]
	max_theme = maximum ()
	
	l = []

	i = 1
	while i <= max_theme:
		l.append (str (i))
		i += 1
	return l
	
if __name__ == '__main__':
	persistance.init ()
	
	print (liste_themes ())
	print (liste_themes_opts ("description","x:chargement","y:plateau"))
	
