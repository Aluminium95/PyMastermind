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
		rep = moteur.proposer_solution(Li)
		if rep == "gagne":
			iconsole.afficher("Mastermind", "Vous avez gagné !!!")
			break
		elif rep == "perdu":
			iconsole.afficher("Mastermind","Vous avez perdu !!!")
			break
		else:
			a,b = rep
			print ("_" * 50) # Afficher à la main ?
			# On peut rafiner en mettant les s si besoin seulement, et ne pas afficher 
			# le texte si la valeur est 0 ...
			iconsole.afficher("Mastermind","Il y a " + str(a) + " bonne(s) couleur(s) et bonne place(s)")
			iconsole.afficher("Mastermind","Il y a " + str(b) + " bonne(s) couleur(s) et mauvaise place(s)")
			iconsole.afficher("Mastermind"," Voulez-vous rejouer ?")
			print ("_" * 50) # Idem ? ...
				    

