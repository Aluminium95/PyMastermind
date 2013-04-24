#-*- coding: utf-8 -*-
# 03/04/2013
# Desmarais Yann 

def separateur ():
	""" Affiche un énorme séparateur !

		@return : None
	"""
	print (100 * "-")

def afficher(acteur,dialogue,t=0):
	""" Affiche une information à l'utilisateur 
	
		@acteur : string = qui parle 
		@dialogue : string = quoi
		
		@return : None
	"""
	# met t tabulations devant le texte ... permet d'intenter !
	formattage = "\t" * t + "- ({0}) : « {1} »"
	print (formattage.format (acteur,dialogue))

def demander(acteur,dialogue,t=0):
	""" Demande une information à l'utilisateur 
		
		@acteur : string = qui demande
		@dialogue : string = quoi 
		
		@return : string = l'information 
	"""
	# met t tabulations devant le texte : indentation !
	formattage = "\t" * t + "# [{0}] ? {1} : "
	# return raw_input (formattage.format (acteur,dialogue))
	return input (formattage.format (acteur,dialogue))

def afficher_liste (acteur,message,liste,t = 0):
	""" Affiche une liste à l'utilisateur """
	afficher (acteur,message,t)
	for i in liste:
		if isinstance (i,tuple):
			print ("\t" * (t + 1) + "{0} - {1}".format (i[0],i[1]))
		else:
			print ("\t" * (t + 1) + "- {0}".format (i))

def afficher_generateur (acteur,message,generateur, t = 0):
	""" Affiche un générateur à l'utilisateur """
	afficher (acteur, message, t)
	for i in generateur:
		if isinstance (i,tuple):
			print ("\t" * (t + 1) + "{0} - {1}".format (i[0],i[1]))
		else:
			print ("\t" * (t + 1) + "- {0}".format (i))

def demander_tableau (n = 4):
	""" Demande un tableau
		
		@n : int = nombre de cases 
		
		@return : [str ...] = le tableau rentré par l'utilisateur 
	"""
	
	i = 0
	Li = []
	afficher ("Entrée tableau","Début du tableau...",1)
	
	while i < n:
		x = demander("Entée Tableau","entrez une couleur",2)
		Li.append(x)
		i = i + 1
	
	afficher ("Entrée tableau","Fin du tableau...",1)
	return Li 
