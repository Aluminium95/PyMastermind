#-*- coding: utf-8 -*-
# 03/04/2013
# Desmarais Yann 



def afficher(acteur,dialogue,t=0):
	""" Affiche une information à l'utilisateur 
	
		@acteur : string = qui parle 
		@dialogue : string = quoi
		
		@return : None
	"""
	formattage = "\t" * t + "- [{0}] : {1}"
	print formattage.format (acteur,dialogue)

def demander(acteur,dialogue,t=0):
	""" Demande une information à l'utilisateur 
		
		@acteur : string = qui demande
		@dialogue : string = quoi 
		
		@return : string = l'information 
	"""
	formattage = "\t" * t + "# [{0}] ? {1}"
	return raw_input (formattage.format (acteur,dialogue))


def demander_tableau ():
	""" Demande un tableau """
	i = 0
	Li = []
	afficher ("Entrée tableau","Début du tableau...",1)
	while i<4:
		x = demander("Entée Tableau","entrez une couleur: ",2)
		Li.append(x)
		i = i+1
	afficher ("Entrée tableau","Fin du tableau...",1)
	return Li 
