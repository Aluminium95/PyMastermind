# -*- coding: utf-8 -*-
#règles du jeu (mode facile, normal et difficile)
#24/04/2013

import persistance
import couleurs

import moteur

from primitives import *


def niveau(niveau):
	text="Voici les regles du mastermind mode " + niveau + ":"
	write(text, False, "center", ("calibri",16,"underline"))

def main_text():
	goto(-133,150)
	text2="- Vous devez deviner le code couleur du jeu."
	texte (text2)
	goto(-132,120)
	dot(10,"red")
	goto(-127,110)
	text3=" : Signifie que la couleur est juste et bien placée."
	texte (text3)
	goto(-132,90)
	dot(10,"black")
	goto(-127,80)
	text4=" : Signifie que la couleur est juste mais mal placée."
	texte (text4)
	goto(-133,50)
    

def nombre_coup(coups):
	text5="- Il y a " + coups + " couleurs selectionnables." 
	texte (text5)

def main_text2():
	text6="- Le code à trouver est composé de 4 couleurs."
	texte (text6)
	goto(-133,-10)
	text7="- Vous avez 10 essais maximum pour le deviner."
	texte (text7)
	goto(20,-40)
	color("red")
	begin_fill()
	text8="Attention,"
	texte (text8)
	end_fill()
	color("black")
	goto(-133,-60)
	text9="si rien n'est indiqué, alors votre réponse est fausse."
	texte (text9)
	goto(-185,-130)
	text10="Panel de couleurs :"
	write(text10, False, "center", ("calibri",15,"underline"))
	goto(-285,-280)

def carre(taille):
	c = 0
	down ()
	while c < 4:
		forward(taille)
		left(90)
		c = c + 1
	up ()


	
def generateur_couleurs (tableau): # C'est lui 
	""" Générateur qui dessine 
		une à une les couleurs 
		du tableau, avec leur nom 
		à côté d'un carré de la-dite 
		couleur

		@tableau : [couleur (fr) ...] = tableau des couleurs

		@return : generator 
	"""
	for i in tableau:
		try:
			color (couleurs.string_to_hexa (i))
		except:
			pass # Une putain d'erreue survient ici !
		begin_fill ()
		polygone (4,10) # Un ... Carré
		end_fill ()
		
		fd (20)
		right (90)
		fd (5)
		texte (i, "petit")
		fd (-5)
		left (90)
		fd (-20)
		yield 

def couleurs_possibles ():
	li = couleurs.liste_couleurs ()
	
	try:
		li = li[0:moteur.get_nombre_couleurs ()]
	except:
		li = li[0:moteur.get_nombre_couleurs_next ()]
	
	g = generateur_couleurs (li)

	colonnes (4,25,120,g)

def regles ():
	"""Affiche les règles ainsi que les aides du jeu. En mode facile.
	(un fond y est inséré)"""
	mode = ""
	
	try:
		mode = moteur.get_mode ()
	except:
		mode = moteur.get_next_mode ()
	
	raz ()
	screensize(600,600,"white")
	
	if mode == "facile":
		bgpic("Images/Regles/ff.gif")
	elif mode == "moyen":
		bgpic ("Images/Regles/fn.gif")
	else:
		bgpic ("Images/Regles/fd.gif")
	
	
	up()
	goto(30,220)
	color("black")
	niveau('facile')
	main_text()
	goto(-133,50)
	nombre_coup('8')
	goto(-133,20)
	main_text2()
	goto (-245,-160)
	
	couleurs_possibles ()

# Cette partie de code ne s'exécute que
# quand le programme est lancé directement 
# ce n'est pas exécuté quand le module 
# est importé, ou quand on génère la doc 
# ... Très utile cette petite astuce !
if __name__ == '__main__':
	persistance.init ()
	couleurs.init ()
	moteur.init ()
	
	regles_difficile ("#000")
	
	mainloop ()
