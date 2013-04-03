#-*- coding: utf-8 -*-
# 03/04/2013
# Desmarais Yann 

import moteur

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

def choisir_code ():
	afficher ("Jeu","Choisir le code ...")
	c = False
	while c == False:
		t = demander_tableau ()
		c = moteur.definir_code (t)
		if c == False:
			afficher ("Jeu","Le moteur a refusé ...")

def jouer():
	afficher ('Jeu',"Devines le code !!!")
	Li=[]
	rep=0
	while True:
		Li=demander_tableau()
		rep=moteur.proposer_solution(Li)
		if rep=="gagne":
			afficher("Jeu:", " Vous avez gagnez !!!")
			break
		elif rep=="perdu":
			afficher("Jeu:","Vous avez perdu !!!")
			break
		else:
			a,b = rep
			print("___________________________________________________")
			afficher("Jeu:",str(a)+" bonne(s) couleur(s) et bonne place(s)")
			afficher("Jeu:",str(b)+" bonne(s) couleur(s) et mauvaise place(s)")
			afficher("Jeu:"," Voulez-vous rejouer ?")
			print("___________________________________________________")
				    

                
