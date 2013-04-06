#-*- coding: utf-8 -*-
# 03/04/2013
# Desmarais Yann 



def afficher(acteur,dialogue):
	""" Affiche une information à l'utilisateur 
	
		@acteur : string = qui parle 
		@dialogue : string = quoi
		
		@return : None
	"""
	print acteur,":",dialogue

def demander(acteur,dialogue):
	""" Demande une information à l'utilisateur 
		
		@acteur : string = qui demande
		@dialogue : string = quoi 
		
		@return : string = l'information 
	"""
	return raw_input("[" + acteur + "]" +" - "+dialogue)


def demander_tableau ():
	""" Demande un tableau """
	i=0
	Li=[]
	afficher ("DEBUG","Début du tableau...")
	while i<4:
		x=demander("jeu","entrez une couleur: ")
		Li.append(x)
		i=i+1
	afficher ("DEBUG","Fin du tableau...")
	return Li




                
