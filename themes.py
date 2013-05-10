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

def liste_themes ():
	# C'est con ... ça génère ["1", "2", ..., "max"]
	max_theme = persistance.get_propriete ("backgrounds", "theme:max")
	
	l = []

	i = 1
	while i <= int (max_theme):
		l.append (str (i))
		i += 1
	return l
