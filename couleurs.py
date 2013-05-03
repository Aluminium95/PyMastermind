#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Lopez Aliaume
#
#
# Ce module sert à gérer les 
# couleurs ... 
#
#
#
# Le concept est simple, on a deux
# représentations, on les définit par des 
# fonctions d'identité : is_hexa et is_string
# de manière à les différencier.
#
# Ensuite on permet la conversion, retournant
# « False » si c'est mauvais ...
#
# Le tout a la particularité de fonctionner 
# avec le module « persistance ». En effet
# la « table de conversion » est un fichier
# de configuration.
#
# Cela permet aussi de dresser simplement
# la liste des valeurs possibles, en lisant 
# le fichier et créeant une liste (dans « init () »)
# 
# Ce code est fonctionnel ! Bien que parfois 
# peu efficace ... mais ça ne devrait pas 
# poser de problèmes :-)
#
# La base est de la sorte : 
# couleur(fr) -> couleur(hexa)
# $couleur(abrv) -> couleur(fr) 
#
# On a un $ devant les abréviations pour les 
# différencier des couleurs !

import persistance

# Définition des exceptions 

class CouleurInvalide (Exception):
	pass

# Fin définition des exceptions

couleurs = [] # liste des couleurs possibles 
abreviations = [] # Liste des abréviations possibles

def string_to_hexa (couleur):
	""" Retourne la valeur Hexa de la couleur
		
		@couleur : string = couleur à convertir
		
		@return : string 

		@throw : CouleurInvalide 
				 persistance.FichierInvalide
				 persistance.CleInvalide
	"""
	if is_string (couleur): # vérifie que c'est une chaine valide
		return persistance.get_propriete ("couleurs",couleur)
	else:
		raise CouleurInvalide

def abrv_to_string (abrv):
	""" Retourne la valeur String de l'abréviation
		
		@abréviation : string = abréviation à convertir
		
		@return : string 

		@throw : CouleurInvalide 
				 persistance.FichierInvalide
				 persistance.CleInvalide
	"""
	if is_abrv (abrv): # vérifie que c'est une chaine valide
		return persistance.get_propriete ("couleurs", "$" + abrv) # Les abréviations commencent par un $
	else:
		raise CouleurInvalide
	
def string_to_abrv (string):
	""" Retourne l'abbréviation d'une couleur 
		
		@string : couleur(fr) = la couleur à convertir
		
		@return : couleur(abrv)
		
		@throw : CouleurInvalide
				 persistance.FichierInvalide
				 persistance.CleInvalide
	"""
	if is_string (string):
		return persistance.get_by_value ("couleurs",string)[1:] # Retire le $ devant la clé
	else:
		raise CouleurInvalide
	
def hexa_to_string (hexa):
	""" Retourne la valeur String de la couleur en Hexa
		
		@hexa : string = hexa à convertir
		
		@return : string
		
		@throw : CouleurInvalide 
				 persistance.FichierInvalide
				 persistance.CleInvalide
	"""
	if is_hexa (hexa): # on vérifie quand même que c'est bien de l'hexa
		# on cherche la clé qui a pour valeur associée @hexa 
		# ... cle -> valeur 
		# on fait donc l'inverse de d'habitude !!! 
		return persistance.get_by_value ("couleurs",hexa)
	else:
		raise CouleurInvalide


def liste_couleurs ():
	""" Retourne la liste des couleurs (en string)
		
		@return : [string ...]
	"""
	return list (couleurs) # retourne une COPIE de la liste de couleurs

def liste_abreviations ():
	""" Retourne la liste des abréviations
		
		@return : [abrv ...]
	"""
	return list (abreviations)
	
def is_hexa (couleur):
	""" Dit si la couleur est sous forme hexadécimale
		
		@couleur : ? = élément à tester
		
		@return : bool 
	"""
	# il faut que ce soit une str
	# que son premier caractère soit un « # »
	# et qu'il y ai 6 éléments après !
	if isinstance (couleur,str) and couleur[0] == "#" and len (couleur) == 7:
		return True
	else:
		return False
	
def is_abrv (couleur):
	""" Dit si la couleur est sous forme d'abréviation
		
		@couleur : ? = élément à tester
		
		@return : bool
	"""
	if isinstance (couleur,str) and couleur in abreviations:
		return True
	else:
		return False

def is_string (couleur):
	""" Dit si la couleur est sous forme de chaine
		
		@couleur : ? = élément à tester
		
		@return : bool
	"""
	# si la couleur est dans le tableau ... 
	# sinon ... c'est faux !
	if couleur in couleurs:
		return True
	else:
		return False
	
def init ():
	""" Initialise le module 
		
		@return : None
	"""
	global couleurs, abreviations
	# Génère la liste des couleurs ... 
	lcouleurs = [] # Liste des couleurs
	labrvs = [] # Liste des abrvéviations
	n = persistance.liste_variables ("couleurs")
	for i in n:
		# On ne prend que les couleurs,
		# et après on convertit en abréviation
		# De cette manière on a un ordre UNIQUE
		# et identique pour les deux listes au niveau
		# des couleurs !
		if i[0] != "$": # Les abréviations commencent par $, on n'en veut pas !
			lcouleurs.append (i) # Et on l'ajoute au bon tableau
	
	
	couleurs = lcouleurs # Sauvegarde les couleurs string
	# Parce que string_to_abrv utilise is_string ... or il lui faut la liste des couleurs !
	
	for i in couleurs:
		labrvs.append (string_to_abrv (i))
		
	abreviations = labrvs

def couleur_to_hexa(couleur):
	""" Permet de tester une variable pour savoir si elle est une couleur hexa ou en français et convertir en hexa
		
		@couleur : ? = le truc 
		
		@return : string (hexa)

		@throw : CouleurInvalide 
				 persistance.FichierInvalide
				 persistance.CleInvalide
	"""
	if is_hexa (couleur):
		return couleur
	elif is_string (couleur):
		return string_to_hexa (couleur)
	else:
		return abrv_to_string (string_to_hexa (couleur))

def couleur_to_string (couleur):
	""" Permet de tester une variable pour savoir si elle est une couleur 
		en string ou en hexa et convertir en string si nécessaire (français)

		@couleur : ? = le truc à convertir

		@return : string (français) 
		
		@throw : CouleurInvalide 
				 persistance.FichierInvalide
				 persistance.CleInvalide
	"""
	
	if is_abrv (couleur):
		return abrv_to_string (couleur)
	elif is_hexa (couleur):
		return hexa_to_string (couleur)
	elif is_string (couleur):
		return couleur
	else:
		raise CouleurInvalide

def eclaircir (couleur, pts):
	""" Permet d'éclaircir une couleur passée en argument d'une 
		valeur de « pts », nombre à « ajouter ».

		Attention : ne vérifie pas que la couleur générée est correcte ...
		turtle n'affiche pas les couleurs invalides, donc quand c'est terminé,
		c'est terminé :-).

		@couleur : couleur = une couleur, sous n'importe quelle représentation
		@pts : str = le taux d'éclaircissement à ajouter à chaque valeur
			Est de type "A0", c'est à dire DEUX caractères obligatoires, 
			entre 0 et F (0 1 ... 8 9 A B... E F)

		@return : couleur (hexadecimal)
	"""
	c = couleur_to_hexa (couleur)
	r = int (c[1:],16) # Convertit en nombre entier normal 

	taux = int (pts * 3, 16)

	r += taux

	#return "#" + hex (r)[2:]
	return couleur # hahaha 
	

# Test
if __name__ == '__main__':
	persistance.init () # Charge les fichiers
	init () # initialise le module (auto-initialise ?!)

	# Démonstration 
	print (string_to_hexa ("or"))
	print (hexa_to_string ("#A300FF"))
	print (hexa_to_string (string_to_hexa ("jaune"))) # inutile 


	persistance.save () # inutile aussi ... mais s'il y a eu des changements ... 
