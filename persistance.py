#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# Lopez Aliaume
# 30/03/2013
# 
# Fichier gérant tout ce qui est persistance 
# des informations dans une sorte de BDD
# 
# 
# L'API est orientée vers les clé => valeur
# et laisse le soin à l'utilisateur de définir
# son propre fonctionnement : il n'y a pas 
# de schémas prédéfinis d'utilisation !
#
#
# BDD :
# [ 
#	["fichier1", ["variable1", "valeur1"], ... , ["variableN","valeurN"]],
#	...
#	["fichierN", ["variable1", "valeur1"], ... , ["variableN","valeurN"]]
# ]
	


# ma variable globale : BDD
persistant = []

def liste_fichiers ():
	""" Retourne les fichiers chargés
		
		@return : [string ...]
	"""
	l = [] # La liste de sortie 
	for i in persistant: # pour chaque fichier chargé
		l.append (i[0]) # On ajoute le nom du fichier 
	return l
	
def liste_variables (fichier):
	""" Retourne toutes les variables dans un fichier
	
		@fichier : string = nom du fichier dans lequel chercher les variables
		
		@return : [string ...]
	"""
	l = False
	for i in persistant: # Pour chaque fichier 
		if i[0] == fichier: # Si le nom du fichier correspond
			l = [] # On crée une liste 
			for j in i[1:]: # On prend tous les éléments du fichier 
				l.append (j[0]) # On récupère seulement les noms de ceux-ci
			break # On casse la boucle 
	return l # On retourne la liste générée (ou False ...)

def charger_fichier (chemin):
	""" Charge un fichier de configuration
		
		@chemin : string = chemin du fichier à charger
		
		@return : "chargement" | "creation"
	"""
	global persistant 
	try: # Cette partie est suceptible de planter 
		f = open (chemin,"r") # On ouvre le fichier en lecture seule
		newlist = [chemin] # On crée la liste du fichier 
	
		for line in f: # Pour chaque ligne du fichier 
			if line != "\n" and line[0] != "#": # On vérifie que la ligne doit être prise en compte 
				s = line[:-1].replace ("\\n","\n").split (" |=> ") # On découpe en deux
				newlist.append (s) # On a le tableau [clé,valeur] d'un élément !
		
		persistant.append (newlist) # On ajoute le fichier 
		return "chargement" 
	except: # Si elle plante 
		new_file (chemin) # On crée un fichier « virtuel » vide 
		return "creation"
		
	
def get_propriete (chemin,nom):
	""" Récupère une propriété
		
		@chemin : string = chemin du fichier dans lequel se trouve la propriété
		@nom : string = nom de la propriété 
		
		@return : string | False
	"""
	for p in persistant: # Pour chaque fichier 
		if p[0] == chemin: # Si le nom correspond 
			for i in p[1:]: # On regarde les éléments du fichier 
				if i[0] == nom: # Si le nom correspond 
					return i[1] # On retourne la valeur !
			break # Si le nom n'existe pas, pas la peine d'aller plus loin ...
	
	return False 

def get_by_value (chemin,val):
	""" Récupère le nom de la propriété contenant la valeur @val
		
		@chemin : string = chemin du fichier dans lequel se trouve la propriété
		@val : string = valeur de la propriété
		
		@return : string | False
	"""
	for p in persistant: # Pour chaque fichier 
		if p[0] == chemin: # si le chemin correspond 
			for i in p[1:]: # On regarde chaque élément
				if i[1] == val: # Si la valeur correspond 
					return i[0] # On retourne la clé 
			break # Si la valeur n'existe pas, pas la peine d'aller plus loin 
	return False
	
def new_file (chemin):
	""" Ajoute un fichier virtuel (enregistré plus tard)
		
		@chemin : string = chemin du fichier à créer 
		
		@return : None
	"""
	global persitant

	l = liste_fichiers () # On récupère la liste des fichiers déjà chargés
	if chemin not in l: # Si le fichier n'est pas dedans
		persistant.append ([chemin]) # On le crée (virtuellement) 

def add_propriete (chemin,nom,val):
	""" Ajoute une propriété, même si elle existe déjà
		
		@chemin : string = chemin du fichier dans lequel se trouve la propriété
		@nom : string = nom de la propriété
		@val : string = valeur de la propriété  
		
		@return : bool = si ça s'est bien passé 
	"""
	global persistant 
	
	for p in persistant: # Pour chaque fichier 
		if p[0] == chemin: # Si le nom correspond
			p.append ([nom,val]) # On ajoute à la fin le coupe [clé,valeur]
			return True
	return False

def set_propriete (chemin,nom,val):
	""" Définit une propriété, et la crée si elle n'existe pas 
		
		@chemin : string = chemin du fichier dans lequel se trouve la propriété
		@nom : string = nom de la propriété
		@val : string = valeur de la propriété  
		
		@return : bool = si ça s'est bien passé 
	"""
	global persistant
	
	for p in persistant: # Pour chaque fichier 
		if p[0] == chemin: # Si le nom correspond 
			for i in p[1:]: # On regarde pour chaque élément
				if i[0] == nom: # Si l'élément a le bon nom
					i[1] = val # On définit sa valeur 
					return True
			p.append ([nom,val]) # Sinon on ajoute à la fin [clé,valeur]
			return True
	return False
	
def save ():
	""" Enregistre les modifications dans les fichiers
	
		@return : bool = si ça s'est bien passé 
	"""
	try:
		for p in persistant: # Pour chaque fichier 
			f = open (p[0],"w") # On ouvre un fichier de son nom en écriture 
			for prop in p[1:]: # Pour chaque propriété 
				# on écrit la ligne correspondante 
				f.write (prop[0] + " |=> " + prop[1].replace ("\n","\\n"))
				f.write ("\n") # Avec un saut de ligne 
			f.close () # Et on ferme le fichier 
	except:
		return False

def set_default_value (chemin,variable,valeur):
	""" Définit une valeur par défaut pour la variable
		qui sera utilisée si elle n'est pas encore définie

		@chemin : string = chemin du fichier 
		@variable : string = nom de la variable
		@valeur : string = valeur de la variable 

		@return : None
	"""
	try: # Cette fonction peut échouer ...
		for p in persistant: # Pour chaque fichier 
			if p[0] == chemin: # Si le nom correspond
				for prop in p[1:]: # On regarde chaque élément
					if prop[0] == variable: # Si le nom correspond
						return True # On retourne Vrai (exsite déjà)
				p.append ([variable,valeur]) # S'il n'exsiste pas, on crée le couple [clé,valeur]
				return True
	except:
		return False

def init ():
	""" fonction d'initialisation du module
	
		@return : None 
	"""
	
	# fichier de configuration globale
	charger_fichier ("config")
	
	# fichier des scores 
	charger_fichier ("scores")
	
	# fichier des couleurs
	charger_fichier ("couleurs")
	
	# fichier des fonds
	charger_fichier("backgrounds")
