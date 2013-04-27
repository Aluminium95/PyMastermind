#-*- coding: utf-8 -*-
# 03/04/2013
# Desmarais Yann 

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
	print (100 * "-")

def afficher(acteur,dialogue,t=0):
	""" Affiche une information à l'utilisateur 
	
		@acteur : string = qui parle 
		@dialogue : string = quoi
		
		@return : None
	"""
	# met t tabulations devant le texte ... permet d'intenter !
	indentation = "\t" * t
	formattage = "- ({0}) : « {1} »"
	
	formattage = formattage.format (acteur,dialogue).replace ("\n", "\n" + indentation + "\t")
	
	print (indentation + formattage)

def demander(acteur,dialogue,t=0):
	""" Demande une information à l'utilisateur 
		
		@acteur : string = qui demande
		@dialogue : string = quoi 
		
		@return : string = l'information 
	"""
	# met t tabulations devant le texte : indentation !
	indentation = "\t" * t
	
	formattage = "# [{0}] ? {1} : "
	
	formattage = formattage.format (acteur, dialogue).replace ("\n", "\n" + indentation + "\t")
	# return raw_input (formattage.format (acteur,dialogue))
	return input (indentation + formattage)

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
			s = indentation + "{0} - {1}".format (i[0],i[1])
		else:
			s = indentation + "- {0}".format (i)
			
		print (s.replace ("\n","\n" + indentation + "\t"))

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
