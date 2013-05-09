#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Lopez Aliaume
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
# BDD : sous forme de dictionnaires
	

# EXCEPTIONS 

class EcritureImpossible (Exception):
	pass

class FichierInvalide (Exception):
	pass

class CleInvalide (Exception):
	pass

class ValeurInvalide (Exception):
	def __init__ (self, fichier, variable):
		self.fichier = fichier
		self.variable = variable


# FIN EXCEPTIONS	

# ma variable globale : BDD
persistant = {} # un dictionnaire

def liste_fichiers ():
	""" Retourne les fichiers chargés
		
		@return : [string ...]
	"""
	l = []
	for i in persistant:
		l.append (i)
	return l
	
def liste_variables (fichier):
	""" Retourne toutes les variables dans un fichier
	
		@fichier : string = nom du fichier dans lequel chercher les variables
		
		@return : [string ...]
		
		@throw : FichierInvalide
	"""
	
	if not isinstance (fichier, str):
		raise FichierInvalide
	
	try:
		f = persistant [fichier]
	except:
		raise FichierInvalide
	else:
		l = []
		for i in f:
			l.append (i)
		return l

def parcourir_cles (fichier):
	""" Retourne un générateur qui 
		retourne les clés d'un fichier
		
		@fichier : str = nom du fichier dans lequel chercher
		
		@return : generator
		
		@throw : FichierInvalide
	"""
	if not isinstance (fichier, str):
		raise FichierInvalide
	
	found = False
	for i in persistant:
		if i[0] == fichier:
			found = True
			for j in i[1:]:
				yield j[0]
		break
	if found == False:
		raise FichierInvalide

def parcourir_valeurs (fichier):
	""" Retourne un générateur qui 
		retourne les valeurs d'un fichier
		
		@fichier : str = nom du fichier dans lequel chercher
		
		@return : generator
		
		@throw : FichierInvalide
	"""
	if not isinstance (fichier, str):
		raise FichierInvalide
	
	found = False
	for i in persistant:
		if i[0] == fichier:
			found = True
			for j in i[1:]:
				yield j[1]
		break
	if found == False:
		raise FichierInvalide
	
def parcourir_fichier (fichier):
	""" Retourne un générateur qui 
		retourne les tuples 
		clé/valeur d'un fichier
		
		@fichier : str = nom du fichier dans lequel chercher
		
		@return : generator
		
		@throw : FichierInvalide
	"""
	if not isinstance (fichier, str):
		raise FichierInvalide
	
	found = False
	for i in persistant:
		if i[0] == fichier:
			found = True
			for j in i[1:]:
				yield (j[0],j[1])
		break
	if found == False:
		raise FichierInvalide
	
def parcourir ():
	""" Retourne un générateur qui 
		retourne successivement 
		des tuples (fichier,clef,valeur)
		pour chaque clef dans tous les 
		fichiers de configuration connus 
		
		@return : generator
	"""
	
	for i in persistance:
		for j in i[1:]:
			yield (i[0],j[0],j[1])
	

def charger_fichier (chemin):
	""" Charge un fichier de configuration
		
		@chemin : string = chemin du fichier à charger
		
		@return : "chargement" | "creation"
		
		@throw : FichierInvalide
	"""
	global persistant 
	
	if not isinstance (chemin, str):
		raise FichierInvalide
	
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
	
		@throw : FichierInvalide et CleInvalide
	"""
	
	if not isinstance (chemin, str):
		raise FichierInvalide
	elif not isinstance (nom, str):
		raise CleInvalide
	
	for p in persistant: # Pour chaque fichier 
		if p[0] == chemin: # Si le nom correspond 
			for i in p[1:]: # On regarde les éléments du fichier 
				if i[0] == nom: # Si le nom correspond 
					return i[1] # On retourne la valeur !
			raise CleInvalide
	raise FichierInvalide

def get_by_value (chemin,val):
	""" Récupère le nom de la propriété contenant la valeur @val
		
		@chemin : string = chemin du fichier dans lequel se trouve la propriété
		@val : string = valeur de la propriété
		
		@return : string

		@throw : FichierInvalide et CleInvalide 
	"""
	
	if not isinstance (chemin, str):
		raise FichierInvalide
	elif not isinstance (val, str):
		raise CleInvalide
	
	
	for p in persistant: # Pour chaque fichier 
		if p[0] == chemin: # si le chemin correspond 
			for i in p[1:]: # On regarde chaque élément
				if i[1] == val: # Si la valeur correspond 
					return i[0] # On retourne la clé 
			raise CleInvalide	
	return FichierInvalide
	
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
		
		@return : None

		@throw :
			FichierInvalide
			CleInvalide
			ValeurInvalide
	"""
	global persistant 
	
	if not isinstance (chemin, str):
		raise FichierInvalide
	elif not isinstance (nom, str):
		raise CleInvalide
	elif not isinstance (val, str):
		raise ValeurInvalide (chemin, nom)
	
	
	for p in persistant: # Pour chaque fichier 
		if p[0] == chemin: # Si le nom correspond
			p.append ([nom,val]) # On ajoute à la fin le coupe [clé,valeur]
			return
	raise FichierInvalide

def set_propriete (chemin,nom,val):
	""" Définit une propriété, et la crée si elle n'existe pas 
		
		@chemin : string = chemin du fichier dans lequel se trouve la propriété
		@nom : string = nom de la propriété
		@val : string = valeur de la propriété  
		
		@return : None

		@throw : 
			FichierInvalide
			CleInvalide
			ValeurInvalide
	"""
	global persistant
	
	if not isinstance (chemin, str):
		raise FichierInvalide
	elif not isinstance (nom, str):
		raise CleInvalide
	elif not isinstance (val, str):
		raise ValeurInvalide (chemin, nom)
	
	
	for p in persistant: # Pour chaque fichier 
		if p[0] == chemin: # Si le nom correspond 
			for i in p[1:]: # On regarde pour chaque élément
				if i[0] == nom: # Si l'élément a le bon nom
					i[1] = val # On définit sa valeur 
					return
			p.append ([nom,val]) # Sinon on ajoute à la fin [clé,valeur]
			return 
	raise FichierInvalide

def save ():
	""" Enregistre les modifications dans les fichiers
	
		@return : None

		@throw : EcritureImpossible
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
		raise EcritureImpossible

def set_default_value (chemin,variable,valeur):
	""" Définit une valeur par défaut pour la variable
		qui sera utilisée si elle n'est pas encore définie

		@chemin : string = chemin du fichier 
		@variable : string = nom de la variable
		@valeur : string = valeur de la variable 

		@return : None

		@throw : FichierInvalide | ValeurInvalide | CleInvalide
	"""
	
	if not isinstance (chemin, str):
		raise FichierInvalide
	elif not isinstance (nom, str):
		raise CleInvalide
	elif not isinstance (val, str):
		raise ValeurInvalide (chemin, nom)
	
	
	try: # Cette fonction peut échouer ...
		for p in persistant: # Pour chaque fichier 
			if p[0] == chemin: # Si le nom correspond
				for prop in p[1:]: # On regarde chaque élément
					if prop[0] == variable: # Si le nom correspond
						return # On ne modifie pas !
				p.append ([variable,valeur]) # S'il n'exsiste pas, on crée le couple [clé,valeur]
				return 
	except:
		raise FichierInvalide
	
def to_graphviz ():
	""" Crée une représentation dans le format graphviz
		de la configuration actuelle
		et la sauve dans un fichier nommé 
		«~config_graph.dot~»
		
		@return : None
		
		@throw : EcritureImpossible
	"""
	
	try:
		f = open ("config_graph.dot","w")
		f.write ("Digraph G { \n")
		fi = 0
		for p in persistant: # Pour chaque fichier 
			f.write ("f{0} [label=\"{1}\"]\n".format (fi,p[0]))
			
			vi = 0
			
			for prop in p[1:]: # Pour chaque propriété 
				
				variable = prop[0].replace ("\"", "\\\"")
				valeur   = prop[1].replace ("\"", "\\\"")
				
				f.write ("var{0}f{1} [label=\"{2}\"]\n".format (vi, fi, variable))
				f.write ("val{0}f{1} [label=\"{2}\"]\n".format (vi, fi, valeur))
				
				f.write ("f{0} -> var{1}f{0} -> val{1}f{0}\n".format (fi,vi))
				
				vi += 1
			fi += 1
		f.write ("\n}")
		f.close ()
	except:
		raise EcritureImpossible

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
	
	# fichier des phrases
	charger_fichier ("phrases")

if __name__ == '__main__':
	init ()
	to_graphviz ()
