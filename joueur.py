#-*- coding: utf-8 -*-
# Fichier du joueur (némésis de ia.py)

import moteur
import iconsole 

def choisir_code ():
	iconsole.afficher ("Mastermind","Le joueur doit choisir le code ...")
	c = False
	while c == False:
		t = iconsole.demander_tableau ()
		c = moteur.definir_code (t)
		if c == False:
			iconsole.afficher ("Joueur","Le moteur a refusé votre proposition ...")
			
def jouer():
	iconsole.afficher ('Mastermind',"Joueur devine le code ...")
	Li = []
	rep = 0
	while True:
		Li = iconsole.demander_tableau()
		rep = moteur.proposer_solution(Li)
		if rep == "gagne":
			iconsole.afficher("Mastermind", "Vous avez gagné !!!")
			break
		elif rep == "perdu":
			iconsole.afficher("Mastermind","Vous avez perdu !!!")
			break
		else:
			a,b = rep
			print("_" * 25)
			iconsole.afficher("Mastermind",str(a)+" bonne(s) couleur(s) et bonne place(s)")
			iconsole.afficher("Mastermind",str(b)+" bonne(s) couleur(s) et mauvaise place(s)")
			iconsole.afficher("Mastermind"," Voulez-vous rejouer ?")
			print("_" * 25)
				    

