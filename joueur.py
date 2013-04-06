#-*- coding: utf-8 -*-
# Fichier du joueur (némésis de ia.py)

import moteur
import iconsole 


def choisir_code ():
	iconsole.afficher ("Jeu","Choisir le code ...")
	c = False
	while c == False:
		t = iconsole.demander_tableau ()
		c = moteur.definir_code (t)
		if c == False:
			iconsole.afficher ("Jeu","Le moteur a refusé ...")
			
def jouer():
	iconsole.afficher ('Jeu',"Devines le code !!!")
	Li=[]
	rep=0
	while True:
		Li= iconsole.demander_tableau()
		rep=moteur.proposer_solution(Li)
		if rep=="gagne":
			iconsole.afficher("Jeu:", " Vous avez gagnez !!!")
			break
		elif rep=="perdu":
			iconsole.afficher("Jeu:","Vous avez perdu !!!")
			break
		else:
			a,b = rep
			print("___________________________________________________")
			iconsole.afficher("Jeu:",str(a)+" bonne(s) couleur(s) et bonne place(s)")
			iconsole.afficher("Jeu:",str(b)+" bonne(s) couleur(s) et mauvaise place(s)")
			iconsole.afficher("Jeu:"," Voulez-vous rejouer ?")
			print("___________________________________________________")
				    

