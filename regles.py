#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Module qui gère l'affichage
# d'un écran de règles


import persistance
import couleurs

import moteur

from primitives import *


def niveau(niveau): #Renvoie le niveau à l'utilisateur
	text="Voici les regles du mastermind mode " + niveau + ":"
	write(text, False, "center", ("calibri",16,"underline"))


def generateur_texte (coups): #génère le texte qui s'affiche dans la fenêtre de Turtle grâce à des générateurs
	text2="- Vous devez deviner le code couleur du jeu."
	texte (text2)
	yield 
	
	up ()
	left (90)
	forward (10)
	dot (10,"red")
	forward (-10)
	right (90)
	up ()
	forward (20)
	text3=" : Signifie que la couleur est juste et bien placée."
	texte (text3)
	yield
	
	up ()
	left (90)
	forward (10)
	dot(10,"black")
	forward (-10)
	right (90)
	up ()
	forward (20)
	text4=" : Signifie que la couleur est juste mais mal placée."
	texte (text4)
	yield
	
	text5="- Il y a " + coups + " couleurs sélectionnables." 
	texte (text5)
	yield
	
	
	text6="- Le code à trouver est composé de 4 couleurs."
	texte (text6)
	yield
	
	
	text7="- Vous avez 10 essais maximum pour le deviner."
	texte (text7)
	yield

def main_text2(): # génère le texte qui s'affiche dans la fenêtre de Turtle sans générateur
	
	goto (20, -40)
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

	
def generateur_couleurs (tableau): 
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
			pass 
		begin_fill ()
		polygone (4,10) # Un Carré
		end_fill ()
		
		fd (20)
		right (90)
		fd (5)
		texte (i, "petit")
		fd (-5)
		left (90)
		fd (-20)
		yield 

def couleurs_possibles (): #répertorie les couleurs possibles selon les niveau
	li = couleurs.liste_couleurs ()
	
	try:
		li = li[0:moteur.get_nombre_couleurs ()]
	except:
		li = li[0:moteur.get_nombre_couleurs_next ()]
	
	g = generateur_couleurs (li)

	colonnes (4,25,120,g)

def regles (mode = False):
	"""Affiche les règles ainsi que les aides du jeu. Selon le niveau sélectionné.
	(un fond y est inséré)"""
	
	if mode == False:
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
	niveau(mode)
	
	nombre_coups = persistance.get_propriete ("config","coups:" + mode)
	
	generateur = generateur_texte (nombre_coups)
	
	goto (-133,150)
	lignes (1, 0, 30, generateur)
	
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
	
	regles ()
	
	mainloop ()
