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
	
	return list (parcourir_cles (fichier))

def parcourir_cles (fichier):
	""" Retourne un générateur qui 
		retourne les clés d'un fichier
		
		@fichier : str = nom du fichier dans lequel chercher
		
		@return : generator
		
		@throw : FichierInvalide
	"""
	if not isinstance (fichier, str):
		raise FichierInvalide
	
	
	try:
		f = persistant[fichier]
	except:
		raise FichierInvalide
	else:
		for i in f:
			yield i

def parcourir_valeurs (fichier):
	""" Retourne un générateur qui 
		retourne les valeurs d'un fichier
		
		@fichier : str = nom du fichier dans lequel chercher
		
		@return : generator
		
		@throw : FichierInvalide
	"""
	if not isinstance (fichier, str):
		raise FichierInvalide
	
	try:
		f = persistant[fichier]
	except:
		raise FichierInvalide
	else:
		for i in f.values ():
			yield i

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
	
	try:
		f = persistant[fichier]
	except:
		raise FichierInvalide
	else:
		for i,j in f.items ():
			yield (i,j)

def parcourir ():
	""" Retourne un générateur qui 
		retourne successivement 
		des tuples (fichier,clef,valeur)
		pour chaque clef dans tous les 
		fichiers de configuration connus 
		
		@return : generator
	"""
	
	for nom,dico in persistance.items ():
		for cle,valeur in dico.items ():
			yield (nom,cle,valeur)

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
		
		persistant[chemin] = {} # On crée le nouveau dico

	
		for line in f: # Pour chaque ligne du fichier 
			if line != "\n" and line[0] != "#": # On vérifie que la ligne doit être prise en compte 
				cle,val = line[:-1].replace ("\\n","\n").split (" |=> ") # On découpe en deux
				persistant[chemin][cle] = val # On ajoute !
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
	
	try:
		f = persistant[chemin]
	except:
		raise FichierInvalide
	else:
		try:
			return f[nom]
		except:
			raise CleInvalide

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
	
	try:
		f = persistant [chemin]
	except:
		raise FichierInvalide
	else:
		for i,j in f.items ():
			if j == val:
				return i
		raise CleInvalide
	
def new_file (chemin):
	""" Ajoute un fichier virtuel (enregistré plus tard)
		
		@chemin : string = chemin du fichier à créer 
		
		@return : None
	"""
	global persitant

	l = liste_fichiers () # On récupère la liste des fichiers déjà chargés
	if chemin not in l: # Si le fichier n'est pas dedans
		persistant[chemin] = {}

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
	
	
	try:
		f = persistant [chemin]
	except:
		raise FichierInvalide
	else:
		f[nom] = val

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
	
	
	try:
		f = persistant [chemin]
	except:
		raise FichierInvalide
	else:
		f[nom] = val


def save ():
	""" Enregistre les modifications dans les fichiers
	
		@return : None

		@throw : EcritureImpossible
	"""
	try:
		for chemin,dico in persistant.items ():
			f = open (chemin, "w")
			for cle,valeur in dico.items ():
				f.write (cle + " |=> " + valeur.replace ("\n","\\n") + "\n")
			f.close ()
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
	
	
	try:
		f = persistant [chemin]
	except:
		raise FichierInvalide
	else:
		f.setdefault (variable, valeur)
	
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
		for p,dico in persistant.items(): # Pour chaque fichier 
			f.write ("f{0} [label=\"{1}\"]\n".format (fi,p))
			
			vi = 0
			
			for c,v in dico.items ():
				
				variable = c.replace ("\"", "\\\"")
				valeur   = v.replace ("\"", "\\\"")
				
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
