#-*- coding: utf-8 -*-
# 03/04/2013

import persistance
import affichage
import moteur
import iconsole
import joueur
import couleurs
import misc

if __name__ == '__main__':
	persistance.init ()
	couleurs.init ()
	# affichage.init ()

	continuer = True
	while continuer == True:
		jcode = iconsole.demander ("main","Tu veux decider du code ?")
		jcode = misc.question_fermee (jcode)

		if jcode == True:
		    joueur.choisir_code ()
		else:
		    joueur.choisir_code ()

		joueur.jouer ()

		rep = iconsole.demander ("main","Tu veux rejouer ?")
		continuer = misc.question_fermee (jcode)
		affichage.reset ()

	persistance.save ()
