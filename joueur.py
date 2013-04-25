#-*- coding: utf-8 -*-
# Fichier du joueur (némésis de ia.py)

import moteur
import iconsole 

def choisir_code ():
	""" Fonciton qui fait choisir au joueur le code secret du 
		mastermind et le définit pour la partie courante

		@return : None
	"""
	iconsole.afficher ("Mastermind","Le joueur doit choisir le code ...")
	c = False
	
	while c == False:
		t = iconsole.demander_tableau ()
		c = moteur.definir_code (t)
		if c == False:
			iconsole.afficher ("Joueur","Le moteur a refusé votre proposition ...")

# Cette fonction devient ... inutile !
	
def jouer ():
	""" Fonction qui fait jouer le joueur au mastermind, c'est à dire
		lui fait deviner le code, jusqu'à ce qu'il perde ou gagne :-)

		@return : None
	"""
	iconsole.afficher ('Mastermind',"Joueur devine le code ...")
	Li = []
	rep = 0

	while True:
		Li = iconsole.demander_tableau()
		rep = moteur.verification_solution (Li)
		if rep == "gagne":
			iconsole.afficher("Mastermind", "Vous avez gagné !!!")
			break
		elif rep == "perdu":
			iconsole.afficher("Mastermind","Vous avez perdu !!!")
			break
		elif rep == False:
			iconsole.afficher ("Mastermind", "Votre proposition n'a pas de sens ...")
		else:
			a,b = rep
			print ("_" * 50) # Afficher à la main ?
			
			# On fait un joli affichage qui dit si on doit mettre un S ou pas ...
			sa = ""
			sb = ""

			if a > 1:
				sa = "s"

			if b > 1:
				sb = "s"
			
			messaga = "Il y a {0} bonne{1} couleur{1} bien placée{1}".format (a,sa)
			messagb = "Il y a {0} bonne{1} couleur{1} mal placée{1}".format (b,sb)

			iconsole.afficher("Mastermind", messaga)
			iconsole.afficher("Mastermind", messagb)
			iconsole.afficher("Mastermind", "Voulez-vous rejouer")
			print ("_" * 50) # Idem ? ...
				    

