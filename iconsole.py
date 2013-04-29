#-*- coding: utf-8 -*-
# 03/04/2013
# Desmarais Yann 

import os

def afficheur (acteur,t=0):
	""" Crée un afficheur avec des 
		variables prédéfinies 
		
		@acteur : str = qui parle
		@t : int = tabulations 
		
		@return : func = fonction qui affiche du texte 
	"""
	def my_aff (s):
		afficher (acteur, s, t)
	
	return my_aff 

def separateur ():
	""" Affiche un énorme séparateur !

		@return : None
	"""
	print (80 * "-") # Devenu ... inutile ?!


def resize (string):
	""" Une fonction qui fait les sauts 
		de ligne automatique pour une phrase 
		trop longue en console 

		@string : str = chaine à découper

		@return : str = la chaine découpée (avec des \n)
	"""
	
	newstring = ""
	
	lastn = 0
	i = 0
	for lettre in string:
		newstring += lettre
		
		i += 1
		
		if lettre == "\n":
			lastn = i
		elif lettre == "\t":
			i += 7 # Une tabulation prend 7 caractères de plus (8 carac au total)
		
		if i - lastn >= 80:
			newstring += "\n"
			lastn = i
		
	return newstring

def afficher(acteur,dialogue,t=0):
	""" Affiche une information à l'utilisateur 
	
		@acteur : string = qui parle 
		@dialogue : string = quoi
		
		@return : None
	"""
	# met t tabulations devant le texte ... permet d'intenter !
	indentation = "\t" * t
	formattage = "- ({0}) : « {1} »"
	
	formattage = indentation + formattage.format (acteur,dialogue)
	
	formattage = resize (formattage)

	formattage = formattage.replace ("\n", "\n" + indentation + "\t")
	
	print (formattage)

def demander(acteur,dialogue,t=0):
	""" Demande une information à l'utilisateur 
		
		@acteur : string = qui demande
		@dialogue : string = quoi 
		
		@return : string = l'information 
	"""
	# met t tabulations devant le texte : indentation !
	indentation = "\t" * t
	
	formattage = "# [{0}] ? {1} : "
	
	formattage = indentation + formattage.format (acteur, dialogue)
	
	formattage = resize (formattage)

	formattage = formattage.replace ("\n", "\n" + indentation + "\t")
	
	
	# return raw_input (formattage.format (acteur,dialogue))
	try:
		return input (formattage)
	except:
		afficher (acteur, "Vous voulez quitter ? Il y a des moyens moins ... brutaux")
		return "quit" # Ou pas ... 

def afficher_liste (acteur,message,generateur, t = 0):
	""" Affiche un générateur de descriptions à l'utilisateur 
	
		@acteur : str = qui affiche 
		@message : str = quoi
		@generateur : generator = le générateur de la liste 
			d'éléments (a,b) avec 
				a : le nom 
				b : la description
			OU
			d'éléments a, quelconques
			
		@return : None
	"""
	afficher (acteur, message, t)
	
	indentation = "\t" * (t + 1)
	
	for i in generateur:
		if isinstance (i,tuple):
			s = resize (indentation + "{0} - {1}".format (i[0],i[1]))
		else:
			s = resize (indentation + "- {0}".format (i))
			
		print (s.replace ("\n","\n" + indentation + "\t" * 2))

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

if os.name == 'nt':
	def clear ():
		""" Clear l'écran de la console,
		
			@return : None
		"""
		os.system ("cls")
else:
	def clear ():
		""" Clear l'écran de la console
			
			@return : None
		"""
		os.system ("clear")
